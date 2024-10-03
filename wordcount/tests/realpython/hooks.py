import webbrowser
from operator import attrgetter
from unittest.mock import Mock

import pytest
from pytest import Config, Item, Parser, Session, TestReport

from .constants import (COMMAND_TASK, MIN_FAILURES_BEFORE_HINT,
                        STASH_REPORT_KEY, TEST_TIMEOUT_SECONDS)
from .models import ExerciseProgress, TestRun, TestStatus
from .resources import Resource
from .view import Display


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        COMMAND_TASK,
        action="store_true",
        help="Show instructions for the current task",
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    # Suppress pytest's default output unless in help mode:
    if not config.getoption("--help"):
        _disable_plugin(config, "terminalreporter")
        # Other plugins are tightly coupled to the terminal reporter:
        config.pluginmanager.register(Mock(), "terminalreporter")

    # Disable stdout/stderr capturing unless explicitly enabled:
    if not any(
        x.startswith("--capture") for x in config.invocation_params.args
    ):
        _disable_plugin(config, "capturemanager")


def pytest_collection_modifyitems(config, items):
    # Discard items not associated with a @task()
    for item in items.copy():
        if not hasattr(item.function, "task"):
            items.remove(item)

    # Ensure the task numbers start at 1 and are contiguous
    if task_numbers := set(item.function.task.number for item in items):
        if min(task_numbers) != 1:
            raise ValueError("task numbers must start at 1")
        if max(task_numbers) != len(task_numbers):
            raise ValueError("task numbers must be contiguous")

    timeout = pytest.mark.timeout(TEST_TIMEOUT_SECONDS, method="signal")
    skip = pytest.mark.skip(reason="The task must be unlocked first")

    progress = ExerciseProgress.from_cache(config.cache)
    for item in items:
        # Apply a default timeout to each test function
        # (can override individual test functions with @pytest.mark.timeout)
        item.add_marker(timeout)

        # Skip functions owned by tasks that haven't been unlocked yet:
        if item.function.task.number > progress.last_unlocked:
            item.add_marker(skip)

    # Order test functions by the task number they belong to:
    items.sort(key=attrgetter("function.task.number"))


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: Item):
    # Store the test result on the corresponding item instance:
    match report := (yield):
        case TestReport(when="setup", outcome="skipped"):
            item.stash[STASH_REPORT_KEY] = report
        case TestReport(when="call"):
            item.stash[STASH_REPORT_KEY] = report
    return report


def pytest_sessionfinish(session: Session):
    if not session.items:
        return

    if session.config.option.cacheclear:
        return

    progress = ExerciseProgress.from_cache(session.config.cache)
    test_run = TestRun.from_session(session)
    display = Display(session.config)

    if session.config.getoption(COMMAND_TASK):
        last_unlocked = test_run.task(progress.last_unlocked)
        display.print(last_unlocked.url)
        webbrowser.open(last_unlocked.url)
        return

    try:
        _ = test_run.status
    except ValueError:
        return  # None of the tests were executed, e.g., --collect-only

    for test in test_run.tests:
        progress.update(test)

    display.summary(progress, test_run)

    if _new_task_unlocked(progress, test_run):
        if progress.last_unlocked < test_run.num_tasks:
            progress.last_unlocked += 1
            next_task = test_run.task(progress.last_unlocked)
            display.unlocked(next_task)
        else:
            display.congratulations()
    else:
        if resources := _get_resources(progress, test_run):
            display.hint(resources)

    # Update cache
    progress.save()


def _disable_plugin(config: Config, plugin_name: str):
    if plugin := config.pluginmanager.getplugin(plugin_name):
        config.pluginmanager.unregister(plugin)


def _new_task_unlocked(progress: ExerciseProgress, test_run: TestRun) -> bool:
    return all(
        test.status is TestStatus.PASSED
        for test in test_run.tests
        if test.task_number <= progress.last_unlocked
    )


def _get_resources(
    progress: ExerciseProgress, test_run: TestRun
) -> list[Resource]:
    return sorted(
        set(
            resource
            for test in test_run.tests
            if test.status in (TestStatus.FAILED, TestStatus.TIMED_OUT)
            and progress.num_failures(test) > MIN_FAILURES_BEFORE_HINT - 1
            and hasattr(test.function, "resources")
            for resource in test.function.resources
        ),
        key=lambda resource: resource.title_pretty,
    )
