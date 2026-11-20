import re
from playwright.sync_api import expect


def test_login_form(page):
    page.goto("/")
    page.fill("#username", "test_user")
    page.fill("#password", "password123")
    page.click("#loginButton")
    expect(page.locator("#successMessage")).to_be_visible()


def test_page_title(page):
    page.goto("/")
    expect(page).to_have_title(re.compile("Локальна сторінка"))


def test_required_fields(page):
    page.goto("/")
    page.click("#loginButton")
    invalid_count = page.locator(":invalid").count()
    assert invalid_count > 0