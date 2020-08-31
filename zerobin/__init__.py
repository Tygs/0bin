from pathlib import Path

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()

ROOT_DIR = Path(__file__).absolute().parent
