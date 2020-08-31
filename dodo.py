import sys

from pathlib import Path
from fnmatch import fnmatch
from subprocess import check_output, STDOUT

from doit.tools import PythonInteractiveAction

try:
    from local_dodo import *
except ImportError:
    pass

ROOT = Path(__file__).absolute().parent
SOURCE_DIR = ROOT / "zerobin/"
DIST_DIR = ROOT / "dist"

ZEROBIN_VERSION = (SOURCE_DIR / "VERSION").read_text().strip()

DOIT_CONFIG = {
    "default_tasks": ["task_compress"],
    "action_string_formatting": "new",
}


def git(*args):
    return check_output(
        ["git", *args], stderr=STDOUT, timeout=3, universal_newlines=True,
    ).rstrip("\n")


def source_files(extensions=None, exclude=()):
    exclude_filter = ["*.pyc", ".*"]
    exclude_filter.extend(exclude)
    extensions = extensions or [".*"]
    for ext in extensions:
        for file in SOURCE_DIR.rglob(f"*{ext}"):
            if not (
                file.is_dir()
                or any(fnmatch(file, pattern) for pattern in exclude_filter)
            ):
                yield file


def task_generate_manifest():
    def generate():
        globs = " ".join(set(f"*{f.suffix}" for f in source_files()))
        globs += " VERSION"
        (ROOT / "MANIFEST.in").write_text(f"recursive-include zerobin {globs}")

    return {
        "targets": [ROOT / "MANIFEST.in"],
        "actions": [generate],
    }


def task_compress():
    main_js = str(SOURCE_DIR / "static/js/main.min.js")
    main_css = str(SOURCE_DIR / "static/css/style.min.css")
    return {
        "targets": [main_js, main_css],
        "file_dep": list(
            str(f) for f in source_files([".css", ".js"], exclude=[main_css, main_js])
        ),
        "actions": [str(ROOT / "compress.sh")],
    }


def task_build():

    return {
        "targets": [DIST_DIR / f"zerobin-{ZEROBIN_VERSION}-py3-none-any.whl"],
        "file_dep": list(str(f) for f in source_files() if ".min." not in str(f)),
        "task_dep": ["compress", "generate_manifest"],
        "actions": ["python setup.py bdist_wheel"],
    }


def task_publish_to_pypi():
    return {
        "task_dep": ["build"],
        "file_dep": [DIST_DIR / f"zerobin-{ZEROBIN_VERSION}-py3-none-any.whl"],
        "actions": ["twine upload ./dist/*.whl"],
    }


def task_bump_version():
    def bump():

        if git("branch", "--show-current") != "master":
            sys.exit("You must be on the branch master to do that")

        git("fetch", "origin", "master")
        if git("git", "rev-list", "HEAD...origin/master", "--count") != "0":
            sys.exit("Cannot push a new version, you need to pull first")

        git_status = git("status", "--porcelain=1").split("\n")
        if not all(
            line.startswith(" ") for line in git_status if not line.startswith("?")
        ):
            sys.exit("Cannot commit the new version: you have changes to be commited.")

        print("Current version is:", ZEROBIN_VERSION)
        action = "0"
        while action not in "123":

            print("What kind of version is it?\n")
            print("1) Major")
            print("2) Minor")
            print("3) Fix")
            action = input("Enter 1, 2 or 3 (Ctrl + C to quit): ")

        new_version = list(map(int, ZEROBIN_VERSION.split(".")))
        action = int(action) - 1
        new_version[action] += 1
        new_version = ".".join(map(str, new_version))

        print("The new version will be:", new_version)
        if input("Ok? [y/N] ").strip().lower() != "y":
            sys.exit("The version has NOT been bumped")

        print("- Updating VERSION file")
        (SOURCE_DIR / "VERSION").write_text(new_version)
        print("- Commiting VERSION file")
        git("commit", "-m", f"Bumping to version {new_version}")
        print(f"- Adding v{new_version} tag")
        git("tag", f"v{new_version}")
        print("- Pushing tag")
        git("push", "origin", "master", "--tag")

    return {
        "actions": [PythonInteractiveAction(bump),],
    }


def task_release_to_pypi():
    return {"task_dep": ["bump_version", "publish_to_pypi"], "actions": []}
