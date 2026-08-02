from pathlib import Path
import logging


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "jarvis.log"


logger = logging.getLogger("JARVIS")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    arquivo = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    arquivo.setFormatter(
        formatter
    )

    console = logging.StreamHandler()

    console.setFormatter(
        formatter
    )

    logger.addHandler(
        arquivo
    )

    logger.addHandler(
        console
    )