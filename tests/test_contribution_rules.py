"""Guard contributor and agent commands, references, and coverage."""

import re
import subprocess
import sys
from pathlib import Path

import pytest
import toml

ROOT_INDEX = 1
ROOT = Path(__file__).resolve().parents[ROOT_INDEX]
CONFIG_FILE = "pyproject.toml"
GUIDE_FILE = "CONTRIBUTING.md"
AGENT_FILE = "AGENTS.md"
ENCODING = "utf-8"
TASK_PATTERN = re.compile(
    r"uv run (?:(?:--no-sync|--extra [\w-]+) )*task ([\w-]+)"
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^\s)]+)\)")
FRAGMENT_SEPARATOR = "#"
SCHEME_SEPARATOR = ":"
TASK_PREFIXES = [
    "uv run task ",
    "uv run --no-sync task ",
    "uv run --extra auto-hint task ",
]
UNKNOWN_TASK = "nonexistent-agent-task"
VALID_TASK = "all"
GUIDE_LINK = "[guide](CONTRIBUTING.md)"
GUIDE_CONTENT = "# Guide\n"
MINIMUM_COVERAGE = 99
TOOL = "tool"
TASKIPY = "taskipy"
TASKS = "tasks"
VARIABLES = "variables"
THRESHOLD = "coveragefailunder"
COVERAGE = "coverage"
RUN = "run"
BRANCH = "branch"
CONFIG = toml.loads((ROOT / CONFIG_FILE).read_text(encoding=ENCODING))
WORKFLOW_FILE = ".github/workflows/main.yml"
SYNC_PREFIX = "run: uv sync"
LOCKED_FLAG = "--locked"


def assert_documented_tasks(text: str) -> None:
    """Reject unknown task names in the documented uv command forms."""
    commands = set(TASK_PATTERN.findall(text))
    assert commands
    assert commands <= CONFIG[TOOL][TASKIPY][TASKS].keys()


def assert_agent_links(text: str, root: Path) -> None:
    """Reject missing local files linked with inline Markdown links."""
    for target in LINK_PATTERN.findall(text):
        filename = target.split(FRAGMENT_SEPARATOR)[0]
        if filename and SCHEME_SEPARATOR not in filename:
            assert (root / filename).is_file(), target


@pytest.mark.parametrize("document", [GUIDE_FILE, AGENT_FILE])
def test_documented_tasks_exist(document: str) -> None:
    """Reject nonexistent tasks in contributor and agent instructions."""
    assert_documented_tasks((ROOT / document).read_text(encoding=ENCODING))


@pytest.mark.parametrize("prefix", TASK_PREFIXES)
def test_documented_tasks_reject_unknown_names(prefix: str) -> None:
    """Reject a stale task name and accept its corrected command."""
    with pytest.raises(AssertionError):
        assert_documented_tasks(prefix + UNKNOWN_TASK)
    assert_documented_tasks(prefix + VALID_TASK)


def test_agent_links_exist() -> None:
    """Keep inline local instruction references connected to real files."""
    assert_agent_links((ROOT / AGENT_FILE).read_text(encoding=ENCODING), ROOT)


def test_agent_links_reject_missing_files(tmp_path: Path) -> None:
    """Reject a dangling reference and accept it after creating its target."""
    with pytest.raises(AssertionError):
        assert_agent_links(GUIDE_LINK, tmp_path)
    (tmp_path / GUIDE_FILE).write_text(GUIDE_CONTENT, encoding=ENCODING)
    assert_agent_links(GUIDE_LINK, tmp_path)


def test_coverage_requirement_is_preserved() -> None:
    """Keep the documented coverage minimum and branch measurement enabled."""
    threshold = CONFIG[TOOL][TASKIPY][VARIABLES][THRESHOLD]
    assert int(threshold) >= MINIMUM_COVERAGE
    assert CONFIG[TOOL][COVERAGE][RUN][BRANCH] is True


def test_coverage_pipeline_is_preserved() -> None:
    """Keep coverage tasks connected to the protected measurement settings."""
    tasks = CONFIG[TOOL][TASKIPY][TASKS]
    assert tasks["all"] == "task lint && task test && task cover"
    assert tasks["cover"]["use_vars"] is True
    assert tasks["test-coverage"] == {
        **tasks["cover"],
        "help": "Run the pytest test suite with coverage tracking",
    }
    assert tasks["cover"]["cmd"] == "{coverage-command}"
    variables = CONFIG[TOOL][TASKIPY][VARIABLES]
    assert "--cov={project}" in variables["coverage-command"]["var"].split()
    assert (
        "--cov-fail-under={coveragefailunder}"
        in variables["coverage-command"]["var"].split()
    )
    assert variables["coverage-command"]["recursive"] is True
    assert variables["project"] == "gator"
    assert CONFIG[TOOL][COVERAGE][RUN]["source"] == ["gator"]
    assert CONFIG[TOOL][COVERAGE][RUN]["omit"] == [
        "tests/*",
        "**/__init__.py",
    ]
    assert (
        CONFIG[TOOL][COVERAGE].get("report", {}).get("exclude_lines", []) == []
    )
    assert (
        CONFIG[TOOL][COVERAGE].get("report", {}).get("exclude_also", []) == []
    )


def test_ci_dependency_resolution_is_locked() -> None:
    """Require dependency installation jobs to honor the committed lockfile."""
    workflow = (ROOT / WORKFLOW_FILE).read_text(encoding=ENCODING)
    commands = [
        line.strip()
        for line in workflow.splitlines()
        if line.strip().startswith(SYNC_PREFIX)
    ]
    assert commands
    assert all(LOCKED_FLAG in command.split() for command in commands)


def test_unregistered_markers_are_rejected(tmp_path: Path) -> None:
    """Verify the active pytest configuration rejects unknown markers."""
    example = tmp_path / "test_unknown_marker.py"
    example.write_text(
        "import pytest\n"
        "@pytest.mark.unknown_contribution_marker\n"
        "def test_example():\n"
        "    assert True\n",
        encoding=ENCODING,
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "--noconftest",
            "-c",
            str(ROOT / "pytest.ini"),
            str(example),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "'unknown_contribution_marker' not found" in result.stdout


@pytest.mark.parametrize(
    ("rule", "source", "accepted"),
    [
        ("N801", "class invalid_name: pass\n", False),
        ("N801", "class ValidName: pass\n", True),
        ("T100", "breakpoint()\n", False),
        ("T100", "import pdb\npdb.set_trace()\n", False),
        ("T100", "from pdb import set_trace\nset_trace()\n", False),
        ("T100", "def ordinary_function(): pass\n", True),
        ("TID251", "import snoop\n", False),
        ("TID251", "from snoop import snoop as trace\n", False),
        ("TID251", "import pathlib\n", True),
    ],
)
def test_contribution_lint_policy(
    rule: str, source: str, accepted: bool
) -> None:
    """Verify contribution lint rules reject violations and allow recovery."""
    assert rule in CONFIG[TOOL]["ruff"]["lint"]["select"]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--config",
            str(ROOT / CONFIG_FILE),
            "--select",
            rule,
            "-",
        ],
        input=source,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (result.returncode == 0) is accepted
    if not accepted:
        assert rule in result.stdout
