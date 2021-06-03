"""
Defence the plant-uml into separate diagram files.

To create HTML from draft case study sections...

::

    python -m markdown -x extra ch_14/drafts/case_study_14.md >ch_14/drafts/case_study_14.html

"""
from contextlib import redirect_stdout
from io import StringIO
import mistune
import toml
import configparser
import re
from pathlib import Path
from typing import TextIO, Iterable, List, NamedTuple, Optional


class Diagram(NamedTuple):
    """One PlantUML diagram."""

    n: int
    code_lines: List[str]

    @property
    def file_name(self):
        return f"fig_{self.n}.uml"

    @property
    def text(self):
        transformed = (self.rewrite(line) for line in self.code_lines)
        return "\n".join(transformed)

    def rewrite(self, line: str) -> str:
        if line == "skinparam handwritten true":
            return "skinparam handwritten false"
        else:
            return line


class FindDiagrams(mistune.Renderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diagrams = []
        self.recent_heading = None
    def block_code(self, code, lang):
        if lang == "plantuml":
            n = len(self.diagrams)
            fenced = (
                ["@startuml", f"'figure {n}: {self.recent_heading}'"]
                + code.splitlines()
                + ["@enduml"]
            )
            self.diagrams.append(Diagram(n, fenced))
        return code
    def header(self, text, level, raw=None):
        self.recent_heading = text


def defence_diagrams():
    working = Path("ch_10") / "drafts"
    source_path = working / "case_study_10.md"

    renderer = FindDiagrams()
    markdown = mistune.Markdown(renderer=renderer)

    text = source_path.read_text()
    markdown(text)
    print(renderer.diagrams)
    for diagram in renderer.diagrams:
        target = working / diagram.file_name
        print(target)
        target.write_text(diagram.text)


class ExtractPython(mistune.Renderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def block_code(self, code, lang):
        if lang == "plantuml":
            return ""
        if ">>>" in code:
            self.count += 1
            return f"\n```{lang if lang else ''}\n{code}\n```\n"
        return ""

    def block_quote(self, text):
        return ""

    def block_html(self, html):
        return ""

    def header(self, text, level, raw=None):
        return f'\n{level*"#"} {text}\n'

    def hrule(self):
        return ""

    def list(self, body, ordered=True):
        return ""

    def list_item(self, text):
        return ""

    def paragraph(self, text):
        return ""

    def table(self, header, body):
        return ""

    def table_row(self, content):
        return ""

    def table_cell(self, content, **flags):
        return ""

def make_example_doc(target_path: Path, examples: str) -> None:
    """Add (or replace) a new target"""
    print(target_path)
    with target_path.open('w') as target_file:
        with redirect_stdout(target_file):
            print(examples)


def update_pyproject_toml(toml_path: Path) -> None:
    """Update the pyproject.toml tool.tox section
    1. Read the toml wrapper
    2. Parse the tox.ini inside the toml
    3. Get the list of *.py and *.md doctest files
    4. Rewrite the tox.ini's [testenv] or referenced [base] section
    5. Save the revised tox.ini into the toml
    6. Save the revised toml wrapper
    """
    # 1. Load the toml wrapper
    parsed_toml = toml.load(toml_path)

    # 2. Parse the config inside
    config = configparser.ConfigParser()
    config.read_string(parsed_toml["tool"]["tox"]["legacy_tox_ini"])

    # 3. Get the list of *.py and *.md doctest files
    abs_test_paths = (
        list((toml_path.parent/"src").glob("*.py"))
        + list((toml_path.parent/"docs").glob("*.md"))
    )
    rel_test_paths = [f.relative_to(toml_path.parent) for f in abs_test_paths]

    # 4. Rwrite the [testenv] or referenced [base] section
    rewrite_section(config, rel_test_paths)

    # 5. Save the revised tox.ini into the toml
    with StringIO() as temp_file:
        config.write(temp_file)
        parsed_toml["tool"]["tox"]["legacy_tox_ini"] = temp_file.getvalue()

    # 6. Rewrite the toml
    print(toml.dumps(parsed_toml))
    backup = toml_path.with_suffix(".toml.bkup")
    if not backup.exists():
        toml_path.rename(backup)
    with toml_path.open('w') as toml_file:
        toml.dump(parsed_toml, toml_file)


class MatchingLines:
    """
    Might be slightly smarter to use ``shlex`` to parse the lines instead of ``re``
    """
    pat = re.compile(r"^(.*)$")
    cmd = "{0}"
    def __init__(self, lines: Optional[List[str]] = None) -> None:
        self.lines: List[str] = lines or []
    def is_match(self, line: str) -> bool:
        if match := self.pat.match(line):
            self.lines.append(line)
            return True
        return False
    def from_path(self, path: Path) -> None:
        self.lines.append(self.cmd.format(str(path)))
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.lines!r})"

class Black(MatchingLines):
    pat = re.compile(r"^\s*black\s+(.*)$")
    cmd = "black {0}"

class Doctest(MatchingLines):
    pat = re.compile(r"^\s*python\s+-m\s+doctest\s+(.*)$")
    cmd = "python -m doctest --option ELLIPSIS {0}"

class Pytest(MatchingLines):
    pat = re.compile(r"^\s*python\s+-m\s+pytest\s*(.*)$")
    cmd = "python -m pytest {0}"

class Mypy(MatchingLines):
    pat = re.compile(r"^\s*mypy\s+(.*)$")
    cmd = "mypy {0}"


def rewrite_section(config: configparser.ConfigParser, doctest_paths: List[Path]) -> None:
    """Enforces a common structure.

    Four patterns:

    -   black
    -   python -m doctest for each *.py and *.md file
    -   python -m pytest -vv
    -   mypy --strict --show-error-codes --python-version 3.9 src

    mypy is optional, a few chapters have a testenv that extends base.
    """
    black_lines = Black()
    doctest_lines = Doctest()
    pytest_lines = Pytest()
    mypy_lines = Mypy()
    other_lines = MatchingLines()

    # Two forms: [testenv] and [testenv:...] that refers to [base]
    # The reference has two subforms [testenv:pyxx] and [testenv:{mypy790, mypy800}-pyxx]
    # The mypy8xx is a moving target.
    testenvs = list(s for s in config.sections() if s.startswith("testenv"))
    if len(testenvs) == 1:
        section = testenvs[0]
    else:
        # Pick one environment as the exemplar...
        extended_commands = config.get(testenvs[0], "commands").splitlines()
        xrefs = list(filter(None, (xref_pat.match(c) for c in extended_commands)))
        section = xrefs[0].group(1)

    # Extract the dependencies option and update the details on mypy800
    deps = config.get(section, "deps")
    # Replace line matching "mypy800: mypy==(.*)" with "mypy800: mypy==0.812"
    new_deps = re.sub(r"^mypy800:\s+mypy==(.+?)$", "mypy800: mypy==0.812", deps, re.M)
    config.set(section, "deps", new_deps)

    # Extract the sequence of commands.
    # These will have been de-indented, it appears.
    commands = config.get(section, "commands")
    for line in filter(None, commands.splitlines()):
        any_match = False
        for p in (black_lines, doctest_lines, pytest_lines, mypy_lines):
            any_match = p.is_match(line)
            if any_match:
                break
        if not any_match:
            raise ValueError(f"Didn't recognize {line!r}")

    # Replace the doctest lines with test_files names.
    new_doctest_lines = Doctest()
    for p in doctest_paths:
        new_doctest_lines.from_path(str(p))

    # Create the revised sequence of commands.
    new_commands = [""]
    for p in (black_lines, new_doctest_lines, pytest_lines, mypy_lines):
        new_commands.extend(p.lines)

    # Replace the config section
    config.set(section, "commands", "\n".join(new_commands))


xref_pat = re.compile(r"\{\[(\w+)\](\w+)\}")


def extract_examples(base: Path) -> None:
    renderer = ExtractPython()
    markdown = mistune.Markdown(renderer=renderer)
    config = configparser.ConfigParser()

    chapters = base.glob("drafts/*.md")
    for source_path in chapters:
        text = source_path.read_text()
        renderer.count = 0
        examples = markdown(text)
        if renderer.count > 0:
            target = source_path.parent.parent / "docs" / source_path.name
            make_example_doc(target, examples)
            toml_path = source_path.parent.parent / "pyproject.toml"
            update_pyproject_toml(toml_path)
            print("---")


def test_make_example_doc(tmp_path, capsys):
    # Given
    text = "hello\nworld\n"
    target_path = tmp_path / "example.md"
    # When
    make_example_doc(target_path, text)
    # Then
    assert target_path.read_text() == text + "\n"
    out, err = capsys.readouterr()
    assert out.splitlines() == [str(target_path)]

def test_rewrite_section():
    # Given
    commands = [
       '\tblack src',
       '\tpython -m doctest --option ELLIPSIS drafts/case_study_3.md',
       '\tpython -m doctest --option ELLIPSIS -v src/model.py',
       '\tpython -m doctest --option ELLIPSIS src/commerce_naive.py',
       '\tpython -m doctest --option ELLIPSIS src/commerce.py',
       '\tpython -m doctest --option ELLIPSIS src/media_model_1.py',
       '\tmypy --strict --show-error-codes src',
    ]
    config_text = (
        '[tox]\nminversion = 3.4.0\nskipsdist = True\nenvlist = {mypy790, mypy800}-{py38, py39}\n\n[base]\ndeps =\n  -rrequirements.txt\n  black\n  pytest==6.2.2\n  tox==3.20.0\n  mypy790: mypy==0.790\n  mypy800: mypy==0.800\nsetenv =\n  PYTHONPATH = {toxinidir}/src\ncommands =\n'
        + "\n".join(commands)
        + '\n[testenv:{mypy790, mypy800}-py38]\ndeps =\n  {[base]deps}\nsetenv =\n  {[base]setenv}\ncommands =\n  {[base]commands}\n  python -m doctest --option ELLIPSIS docs/examples_38.md\n\n[testenv:{mypy790, mypy800}-py39]\ndeps =\n  {[base]deps}\nsetenv =\n  {[base]setenv}\ncommands =\n  {[base]commands}\n  python -m doctest --option ELLIPSIS docs/examples.md\n\n\n'
    )
    config = configparser.ConfigParser()
    config.read_string(config_text)
    doctest_paths = [
        Path("docs") / "new_case_study_3.md",
        Path("src") / "model.py",
        Path("src") / "commerce_naive.py",
        Path("src") / "commerce.py",
        Path("src") / "media_model_1.py",
    ]
    # When
    rewrite_section(config, doctest_paths)
    # Then
    assert config.get("base", "commands").splitlines() == [
        '',
        'black src',
        'python -m doctest --option ELLIPSIS docs/new_case_study_3.md',
        'python -m doctest --option ELLIPSIS src/model.py',
        'python -m doctest --option ELLIPSIS src/commerce_naive.py',
        'python -m doctest --option ELLIPSIS src/commerce.py',
        'python -m doctest --option ELLIPSIS src/media_model_1.py',
        'mypy --strict --show-error-codes src',
    ]

def test_update_pyproject_toml(tmp_path):
    # Given
    toml_dict = {
        'project': {
            'name': 'classifier',
            'version': '2021.4.0',
            'description': 'Python 3 Object-Oriented Programming, 4th ed., Chapter 3',
            'readme': 'README.rst',
            'requires-python': '>=3.8',
            'license': {'file': 'LICENSE.txt'},
            'keywords': ['k-NN', 'object-oriented design'],
            'authors': [{'email': 'slott56@gmail.com'}, {'name': 'Steven F. Lott'}]
        },
        'tool': {
            'tox': {
                'legacy_tox_ini': '[tox]\nminversion = 3.4.0\nskipsdist = True\nenvlist = {mypy790, mypy800}-{py38, py39}\n\n[base]\ndeps =\n  -rrequirements.txt\n  black\n  pytest==6.2.2\n  tox==3.20.0\n  mypy790: mypy==0.790\n  mypy800: mypy==0.800\nsetenv =\n  PYTHONPATH = {toxinidir}/src\ncommands =\n  black src\n  python -m doctest --option ELLIPSIS drafts/case_study_3.md\n  python -m doctest --option ELLIPSIS -v src/model.py\n  python -m doctest --option ELLIPSIS src/commerce_naive.py\n  python -m doctest --option ELLIPSIS src/commerce.py\n  python -m doctest --option ELLIPSIS src/media_model_1.py\n  mypy --strict --show-error-codes src\n\n[testenv:{mypy790, mypy800}-py38]\ndeps =\n  {[base]deps}\nsetenv =\n  {[base]setenv}\ncommands =\n  {[base]commands}\n  python -m doctest --option ELLIPSIS docs/examples_38.md\n\n[testenv:{mypy790, mypy800}-py39]\ndeps =\n  {[base]deps}\nsetenv =\n  {[base]setenv}\ncommands =\n  {[base]commands}\n  python -m doctest --option ELLIPSIS docs/examples.md\n\n\n'
            }
        }
    }
    target_path = tmp_path / "pyproject.toml"
    with target_path.open('w') as target_file:
        toml.dump(toml_dict, target_file)
    # Given
    src_path = (tmp_path / "src")
    src_path.mkdir()
    (src_path/"f1.py").write_text("#! f1.py")
    (src_path/"f2.py").write_text("#! f2.py")
    (src_path/"f3.py").write_text("#! f3.py")
    docs_path = (tmp_path / "docs")
    docs_path.mkdir()
    (src_path/"examples.md").write_text("# examples.md")
    # When
    update_pyproject_toml(target_path)
    # Then
    expected_toml_dict = {}
    expected_toml_dict['project'] = toml_dict['project']
    expeected_legacy_tox_ini = (
        '[tox]\n'
        'minversion = 3.4.0\n'
        'skipsdist = True\n'
        'envlist = {mypy790, mypy800}-{py38, py39}\n'
        '\n'
        '[base]\n'
        'deps = \n'
        '\t-rrequirements.txt\n'
        '\tblack\n'
        '\tpytest==6.2.2\n'
        '\ttox==3.20.0\n'
        '\tmypy790: mypy==0.790\n'
        '\tmypy800: mypy==0.812\n'
        'setenv = \n'
        '\tPYTHONPATH = {toxinidir}/src\n'
        'commands = \n'
        '\tblack src\n'
        '\tpython -m doctest --option ELLIPSIS src/f1.py\n'
        '\tpython -m doctest --option ELLIPSIS src/f3.py\n'
        '\tpython -m doctest --option ELLIPSIS src/f2.py\n'
        '\tmypy --strict --show-error-codes src\n'
        '\n'
        '[testenv:{mypy790, mypy800}-py38]\n'
        'deps = \n'
        '\t{[base]deps}\n'
        'setenv = \n'
        '\t{[base]setenv}\n'
        'commands = \n'
        '\t{[base]commands}\n'
        '\tpython -m doctest --option ELLIPSIS docs/examples_38.md\n'
        '\n'
        '[testenv:{mypy790, mypy800}-py39]\n'
        'deps = \n'
        '\t{[base]deps}\n'
        'setenv = \n'
        '\t{[base]setenv}\n'
        'commands = \n'
        '\t{[base]commands}\n'
        '\tpython -m doctest --option ELLIPSIS docs/examples.md\n'
        '\n'
    )
    expected_toml_dict['tool'] = {"tox": {"legacy_tox_ini": expeected_legacy_tox_ini}}
    new_toml_dict = toml.load(target_path)
    assert new_toml_dict == expected_toml_dict
    # Then
    assert (tmp_path / "pyproject.toml.bkup").exists()


if __name__ == "__main__":
    extract_examples(Path.cwd()/"ch_13")
