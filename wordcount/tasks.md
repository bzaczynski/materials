- [x] Reading data from the standard input: `wordcount`
- [x] Reading from a single file: `wordcount file1.txt`
- [x] Supporting the dash character: `wordcount -`
- [x] Reading from multiple files
- [x] Including a total summary when more than one file
- [x] Repeating the same file
- [x] Mixing files with dashes
- [x] Handling missing files and directories
- [x] Dealing with Unicode characters
- [x] Formatting the numbers according to max digits
- [x] Selecting the counts
    - [x] Single options: `--lines`, `--words`, `--bytes`
    - [x] Formatting is still applied
    - [x] Can mix with files and stdin
- [ ] Add the extra `--chars` option
- [ ] Order is always the same
- [ ] Fix docstring of parametrized (!)

TODO: Make the tests run _much_ faster.
TODO: Give some feedback, like why the assertion is failing (expected vs actual)
TODO: docstrings and parametrized tests!


Checklist:

- [x] Extract custom pytest hooks from `conftest.py` in the redis-challenge prototype into a reusable pytest-realpython plugin that can be maintained separately from the challenges
- [x] Refactor the plugin into modular pieces, simplifying the TUI for a streamlined user experience (Essentially, the user only needs to know about the `pytest` command)
- [x] Implement various sanity checks for the plugin to make developing future challenges more reliable 
- [x] Modify the plugin to integrate more tightly with the Real Python CMS instead of relying on the README file and naming conventions
- [x] Add the ability to open a CMS lesson corresponding to the current task inside the user's default web browser from the CLI using `pytest --task`
- [x] Pretty print the acceptance criteria based on the names of the corresponding test functions or fall back to using docstrings where available in order to allow punctuation and special characters to appear in the summary
- [x] Associate various kinds of Real Python resources with tasks or their individual acceptance criteria and display them after a few unsuccessful attempts as a form of help for the user
- [x] Implement the unlocking mechanism for the next task upon completion of the current task so that the user only sees relevant acceptance criteria in the summary
- [ ] Display helpful hints on failed assertions
- [x] Implement a sample solution to the challenge
- [x] Unwind the complete solution into a number of incremental steps that are small enough to follow easily on the CMS
- [ ] (==in progress==) Implement thorough acceptance criteria as pytest assertions for each task
- [ ] Refactor the acceptance criteria to make the subsequent test runs a lot faster
- [x] Set up a placeholder text-based course for the coding challenge on the CMS
- [ ] (==in progress==) Create a lesson outlining the goal and acceptance criteria for each task on the CMS
- [ ] Hook up each lesson on the CMS to the appropriate pytest assertions
- [ ] Create the corresponding solution lessons for each task, detailing the necessary steps with brief explanations (This may end up in either text or video format, whichever is quicker to set up.)
- [x] Prepare the project's scaffolding in the realpython/materials repository 
- [x] Leverage GitHub Codepages for running the individual challenges in the materials monorepo through dedicated `devcontainer.json` configurations as a convenience for beginners who don't want to or know how to run the challenge locally
- [ ] Make a (cookiecutter?) template for the coding challenge project to allow quick bootstrapping of future challenges
- [ ] Extract the pytest-realpython plugin from the `tests/` folder into its own Git repository, set up CI/CD automation, publish to PyPI, etc.
