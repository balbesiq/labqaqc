def test_full_page(page, assert_snapshot):
    page.goto("/")
    assert_snapshot(page.screenshot(), "index-page.png")


def test_h1_element(page, assert_snapshot):
    page.goto("/")
    assert_snapshot(page.locator("h1").screenshot(), "index-page-element-h1.png")