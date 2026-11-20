import re
from playwright.sync_api import expect


def test_site_title(page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))


def test_nav_menu(page):
    page.goto("https://playwright.dev/")
    expect(page.locator("nav").first).to_be_visible()


def test_get_started_link(page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page).to_have_url(re.compile("docs/intro"))