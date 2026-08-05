from playwright.sync_api import sync_playwright
from app.config import PROFILE_PATH


def launch_browser():

    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=PROFILE_PATH,
        channel="chrome",
        headless=False
    )

    page = context.pages[0] if context.pages else context.new_page()

    return playwright, context, page