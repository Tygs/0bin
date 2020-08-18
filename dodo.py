from pathlib import Path

import zerobin


ROOT = Path(__file__).absolute().parent
SOURCE_DIR = ROOT / "zerobin/"
DIST_DIR = ROOT / "dist"


def source_files(extensions=None):
    extensions = extensions or [".*"]
    for ext in extensions:
        for file in SOURCE_DIR.rglob(f"*{ext}"):
            if (
                not file.suffix.endswith("pyc")
                and not file.is_dir()
                and not "/." in str(file)
            ):
                yield file


def generate_manifest():
    extensions = " ".join(set(f"*{f.suffix}" for f in source_files()))
    (ROOT / "MANIFEST.in").write_text(f"recursive-include zerobin {extensions}")


def task_compress():
    return {
        "targets": [
            str(SOURCE_DIR / "static/js/main.min.js"),
            str(SOURCE_DIR / "static/css/style.min.css"),
        ],
        "file_dep": list(str(f) for f in source_files([".css", ".js"])),
        "actions": [str(ROOT / "compress.sh")],
    }


def task_build():

    return {
        "targets": [DIST_DIR / f"zerobin-{zerobin.__version__}-py3-none-any.whl"],
        "file_dep": list(str(f) for f in source_files() if ".min." not in str(f)),
        "actions": [task_compress, generate_manifest, "python setup.py bdist_wheel",],
    }

