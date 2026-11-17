import re
import shutil
from contextlib import contextmanager
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config.config import HEADLESS
from utils.logger import logger

ARTIFACTS = Path("artifacts")


def _save(name):
    return re.sub(r"[^\w,-]", "_", name)


def pytest_sessionstart(session):
    if hasattr(session.config, "workerinput"):
        return
    if ARTIFACTS.exists():
        shutil.rmtree(ARTIFACTS)
    for sub in ("screenshots", "videos", "traces"):
        (ARTIFACTS / sub).mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            shot_dir = ARTIFACTS / "screenshots"
            shot_dir.mkdir(parents=True, exist_ok=True)
            shot_path = shot_dir / f"{_save(item.name)}.png"
            page.screenshot(path=shot_path, full_page=True)
            logger.info("Screenshot is saved %s", shot_path)


@contextmanager
def _ignore_errors(msg):
    try:
        yield
    except Exception:  # noqa: BLE001
        logger.exception(msg)


@pytest.fixture
def traced_context(pw_browser, request):
    video_dir = ARTIFACTS / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)

    context = pw_browser.new_context(record_video_dir=video_dir)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    try:
        yield context
    finally:
        failed = any(
            getattr(request.node, f"rep_{phase}", None)
            and getattr(request.node, f"rep_{phase}").failed
            for phase in ("setup", "call")
        )

        pages = context.pages
        trace_path = None
        if failed:
            trace_dir = ARTIFACTS / "traces"
            trace_dir.mkdir(parents=True, exist_ok=True)
            trace_path = trace_dir / f"{_save(request.node.nodeid)}.zip"

        with _ignore_errors("Failed to stop tracing"):
            context.tracing.stop(path=trace_path)

        with _ignore_errors("Failed to close browser context"):
            context.close()

        if not failed:
            for page in pages:
                if page.video:
                    with _ignore_errors("Failed to delete recorded video"):
                        page.video.delete()


@pytest.fixture(scope="session")
def pw_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(traced_context):
    page = traced_context.new_page()
    yield page
