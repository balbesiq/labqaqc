import io
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = Path(__file__).resolve().parent / "snapshots"


def pytest_addoption(parser):
    parser.addoption("--update-snapshots", action="store_true",
                     help="Оновити еталонні скриншоти")


@pytest.fixture(scope="session", autouse=True)
def local_server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000",
         "--directory", str(ROOT / "public")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        try:
            socket.create_connection(("localhost", 3000), timeout=0.2).close()
            break
        except OSError:
            time.sleep(0.1)
    yield
    proc.terminate()


@pytest.fixture
def assert_snapshot(request, page, browser_name):
    update = request.config.getoption("--update-snapshots")
    vp = page.viewport_size or {"width": 0, "height": 0}
    folder = SNAP_DIR / f"{browser_name}-{vp['width']}x{vp['height']}"

    def _check(image_bytes: bytes, name: str):
        path = folder / name
        if update:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(image_bytes)
            return
        if not path.exists():
            pytest.fail(f"Немає еталона {path}. Запустіть: pytest --update-snapshots")

        expected = Image.open(path).convert("RGB")
        actual = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        if expected.size != actual.size:
            actual.save(path.with_suffix(".actual.png"))
            pytest.fail(f"Різні розміри: {expected.size} vs {actual.size}")

        diff = ImageChops.difference(expected, actual)
        if diff.getbbox() is not None:
            actual.save(path.with_suffix(".actual.png"))
            diff.save(path.with_suffix(".diff.png"))
            pytest.fail(f"Скриншот відрізняється від еталона: {path.name}")

    return _check