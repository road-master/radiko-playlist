"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
from pathlib import Path
import platform
import shutil
from typing import Any, cast, Dict, List
import webbrowser

from invoke import Context, task
from invoke.exceptions import Failure
from invoke.runners import Result
import tomli

ROOT_DIR = Path(__file__).parent
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("radikoplaylist")
SETUP_PY = ROOT_DIR.joinpath("setup.py")
TASKS_PY = ROOT_DIR.joinpath("tasks.py")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SETUP_PY, TASKS_PY, SOURCE_DIR, TEST_DIR]]


def _delete_file(file: Path) -> None:
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


@task(help={"check": "Checks if source is formatted without applying changes"})
def style(context: Context, check: bool = False) -> None:
    """Format code."""
    for result in [
        docformatter(context, check),
        isort(context, check),
        autoflake(context, check),
        pipenv_setup(context, check),
        black(context, check),
    ]:
        if result.failed:
            raise Failure(result)


@task
def docformatter(context: Context, check: bool = False) -> Result:
    """Runs docformatter.

    This function includes hard coding of line length.
    see:
    - Add pyproject.toml support for config (Issue #10) by weibullguy · Pull Request #77 · PyCQA/docformatter
      https://github.com/PyCQA/docformatter/pull/77
    """
    parsed_toml = tomli.loads(Path("pyproject.toml").read_text("UTF-8"))
    config = parsed_toml["tool"]["docformatter"]
    list_options = build_list_options_docformatter(config, check)
    docformatter_options = " ".join(list_options)
    return cast(
        Result, context.run("docformatter {} {}".format(docformatter_options, " ".join(PYTHON_DIRS)), warn=True)
    )


class DocformatterOption:
    def __init__(self, list_str: List[str], enable: bool) -> None:
        self.list_str = list_str
        self.enable = enable


def build_list_options_docformatter(config: Dict[str, Any], check: bool) -> List[str]:
    """Builds list of docformatter options."""
    docformatter_options = (
        DocformatterOption(["--recursive"], "recursive" in config and config["recursive"]),
        DocformatterOption(["--wrap-summaries", str(config["wrap-summaries"])], "wrap-summaries" in config),
        DocformatterOption(["--wrap-descriptions", str(config["wrap-descriptions"])], "wrap-descriptions" in config),
        DocformatterOption(["--check"], check),
        DocformatterOption(["--in-place"], not check),
    )
    return [
        item
        for docformatter_option in docformatter_options
        if docformatter_option.enable
        for item in docformatter_option.list_str
    ]


def autoflake(context: Context, check: bool = False) -> Result:
    """Runs autoflake."""
    autoflake_options = "--recursive {}".format("--check" if check else "--in-place")
    return cast(Result, context.run("autoflake {} {}".format(autoflake_options, " ".join(PYTHON_DIRS)), warn=True))


def isort(context: Context, check: bool = False) -> Result:
    """Runs isort."""
    isort_options = "--recursive {}".format("--check-only --diff" if check else "")
    return cast(Result, context.run("isort {} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True))


def pipenv_setup(context: Context, check: bool = False) -> Result:
    """Runs pipenv-setup."""
    isort_options = "{}".format("check --strict" if check else "sync --pipfile")
    return cast(Result, context.run("pipenv-setup {}".format(isort_options), warn=True))


def black(context: Context, check: bool = False) -> Result:
    """Runs black."""
    black_options = "{}".format("--check --diff" if check else "")
    return cast(Result, context.run("black {} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True))


@task
def lint_flake8(context: Context) -> None:
    """Lint code with flake8."""
    context.run("flake8 {} {}".format("--radon-show-closures", " ".join(PYTHON_DIRS)))


@task
def lint_pylint(context: Context) -> None:
    """Lint code with pylint."""
    context.run("pylint {}".format(" ".join(PYTHON_DIRS)))


@task
def lint_mypy(context: Context) -> None:
    """Lint code with mypy."""
    context.run("mypy {}".format(" ".join(PYTHON_DIRS)))


@task
def lint_bandit(context: Context) -> None:
    """Lints code with bandit."""
    space = " "
    context.run("bandit --recursive {}".format(space.join([str(p) for p in [SOURCE_DIR, TASKS_PY]])), pty=True)
    context.run("bandit --recursive --skip B101 {}".format(TEST_DIR), pty=True)


@task
def lint_dodgy(context: Context) -> None:
    """Lints code with dodgy."""
    context.run("dodgy --ignore-paths csvinput", pty=True)


@task
def lint_pydocstyle(context: Context) -> None:
    """Lints code with pydocstyle."""
    context.run("pydocstyle .", pty=True)


@task(lint_bandit, lint_dodgy, lint_flake8, lint_pydocstyle)
def lint(_context: Context) -> None:
    """Run all linting."""


@task(lint_mypy, lint_pylint)
def lint_deep(_context: Context) -> None:
    """Runs deep linting."""


@task
def radon_cc(context: Context) -> None:
    """Reports code complexity."""
    context.run("radon cc {}".format(" ".join(PYTHON_DIRS)))


@task
def radon_mi(context: Context) -> None:
    """Reports maintainability index."""
    context.run("radon mi {}".format(" ".join(PYTHON_DIRS)))


@task(radon_cc, radon_mi)
def radon(_context: Context) -> None:
    """Reports radon."""


@task
def xenon(context: Context) -> None:
    """Check code complexity."""
    context.run(("xenon" " --max-absolute A" "--max-modules A" "--max-average A" "{}").format(" ".join(PYTHON_DIRS)))


@task
def test(context: Context) -> None:
    """Run tests."""
    pty = platform.system() == "Linux"
    context.run("pytest", pty=pty)


@task(help={"publish": "Publish the result via coveralls", "xml": "Export report as xml format"})
def coverage(context: Context, publish: bool = False, xml: bool = False) -> None:
    """Create coverage report."""
    context.run("coverage run --source {} -m pytest".format(SOURCE_DIR))
    context.run("coverage report")
    if publish:
        # Publish the results via coveralls
        context.run("coveralls")
        return
    # Build a local report
    if xml:
        context.run("coverage xml")
    else:
        context.run("coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task
def clean_build(context: Context) -> None:
    """Clean up files from package building."""
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    context.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(context: Context) -> None:
    """Clean up python file artifacts."""
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    context.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(_context: Context) -> None:
    """Clean up files from testing."""
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests])
def clean(_context: Context) -> None:
    """Runs all clean sub-tasks."""


@task(clean)
def dist(context: Context) -> None:
    """Build source and wheel packages."""
    context.run("python setup.py sdist")
    context.run("python setup.py bdist_wheel")
