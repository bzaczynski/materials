from pytest import Config
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn
from rich.progress import Progress as ProgressBar
from rich.progress import TextColumn
from rich.tree import Tree

from .models import ExerciseProgress, Task, TestRun, TestStatus
from .readme import Readme
from .resources import Resource


class Display:
    def __init__(self, config: Config) -> None:
        self._readme = Readme(config)
        self._console = Console(force_terminal=True)

    def print(self, *args, **kwargs) -> None:
        self._console.print(*args, **kwargs)

    def hint(self, resources: list[Resource]) -> None:
        lines = [
            "\N{ELECTRIC LIGHT BULB} Need help? Check out these resources:",
            *[f"- {resource}" for resource in resources],
        ]
        self.print(Markdown("\n".join(lines)))

    def unlocked(self, next_task: Task) -> None:
        self.print("Yay! You've unlocked another task \N{PARTY POPPER}")
        self.print(
            Markdown(f"\N{WHITE RIGHT POINTING BACKHAND INDEX} {next_task}")
        )

    def congratulations(self) -> None:
        self.print(
            "Congratulations! You've completed the exercise "
            "\N{FACE WITH PARTY HORN AND PARTY HAT}"
        )

    def summary(self, progress: ExerciseProgress, test_run: TestRun) -> None:
        status_color = _color(test_run.status)
        self.print(
            Panel(
                Group(
                    _legend(),
                    "",
                    _tree(progress, test_run),
                    "",
                    _progress_bar(test_run, status_color),
                ),
                title=f"[b]{self._readme.exercise_name}[/b]",
                border_style=status_color,
                expand=False,
            )
        )


def _legend() -> str:
    return (
        "[b]Status Indicators[/]\n"
        "[green]\N{CHECK MARK} Completed  "
        "[red]\N{BALLOT X} Failed  "
        "[gold1]\N{STOPWATCH} Timed out  "
        "[grey37]\N{LOCK} Locked"
    )


def _tree(progress: ExerciseProgress, test_run: TestRun) -> Tree:
    tree = Tree("[bold]Tasks[/]")
    for task_number, task_tests in test_run.tests_by_task:
        task_tests = tuple(task_tests)
        test_function = task_tests[0].function
        if test_function and hasattr(test_function, "task"):
            task = test_function.task
            if task_number > progress.last_unlocked:
                tree.add(
                    f"[grey37] \N{LOCK} [b]Task {task_number}: {task.name}[/]"
                )
            else:
                task_status = test_run.task_status(task_number)
                color = _color(task_status)
                icon = _icon(task_status)
                branch = tree.add(
                    f"[{color}][b]{icon} Task {task_number}: {task.name}[/]"
                )
                for test in task_tests:
                    color = _color(test.status)
                    icon = _icon(test.status)
                    branch.add(f"[{color}]{icon} {test.pretty_name}[/]")
    return tree


def _progress_bar(test_run: TestRun, color: str) -> ProgressBar:
    progress_bar = ProgressBar(
        TextColumn("[bold][progress.description]{task.description}[/]"),
        BarColumn(complete_style=color, finished_style="green"),
        TextColumn(
            f"[progress.percentage][{color}]{{task.percentage:>3.0f}}%"
        ),
        expand=True,
    )
    task_id = progress_bar.add_task("Progress", total=test_run.num_tests)
    progress_bar.update(task_id, completed=test_run.num_passed)
    return progress_bar


def _color(status: TestStatus) -> str:
    return {
        TestStatus.PASSED: "green",
        TestStatus.FAILED: "red",
        TestStatus.TIMED_OUT: "gold1",
        TestStatus.SKIPPED: "grey37 strike",
    }.get(status, "#ffffff")


def _icon(status: TestStatus) -> str:
    return {
        TestStatus.PASSED: "\N{CHECK MARK}",
        TestStatus.FAILED: "\N{BALLOT X}",
        TestStatus.TIMED_OUT: "\N{STOPWATCH}",
    }.get(status, "")
