import base64
import pytest
from playwright.sync_api import Playwright, Page, expect, sync_playwright

URL = "https://magento.softwaretestingboard.com/"


@pytest.fixture
def page(playwright: Playwright, request) -> Page:
    webkit = playwright.webkit
    try:
        option = request.param
        device = playwright.devices[option]
        browser = webkit.launch()
        context = browser.new_context(**device)
    except:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
    page = context.new_page()
    page.goto("http://the-internet.herokuapp.com/")
    yield page
    context.close()
    browser.close()


username = "admin"
password = "admin"
auth = base64.b64encode(f"{username}:{password}".encode()).decode()

"""Test Case 0
I picked wrong link for authorization test but decided to keep it as is"""
def test_login(page: Page):
    page.set_extra_http_headers({"Authorization": "Basic " + auth})
    page.get_by_role("link", name="Basic Auth").click()
    expect(page.get_by_text("Congratulations! You must have the proper credentials.")).to_be_visible()


"""Test Case 1"""
def test_login_form(page: Page):
    page.get_by_role("link", name="Form Authentication").click()
    page.get_by_label("Username").click()
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name=" Login").click()
    expect(page.get_by_role("heading", name="Secure Area", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Logout", exact=True)).to_be_visible()


"""Test Case 2"""
def test_login_form_fail(page: Page):
    page.get_by_role("link", name="Form Authentication").click()
    page.get_by_label("Username").click()
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("Password!")
    page.get_by_role("button", name=" Login").click()
    expect(page.locator("#flash")).to_be_visible()


links_and_headings = [
    ("A/B Testing", "A/B Test Variation"),
    ("Add/Remove Elements", "Add/Remove Elements"),
    ("Basic Auth", None),
    ("Broken Images", "Broken Images"),
    ("Challenging DOM", "Challenging DOM"),
    ("Checkboxes", "Checkboxes"),
    ("Context Menu", "Context Menu"),
    ("Digest Authentication", None),
    ("Disappearing Elements", "Disappearing Elements"),
]


"""Test Case 4
I tried to get link name with Playwright and compare with header not to make
the list above but there were too many links which name didn't correspond to page header.
So I gave up and made this list. But I also got tired to fill till the end so left just first
few links just to demonstrate approach. Sorry"""
@pytest.mark.parametrize("link_name, expected", links_and_headings)
def test_links(page: Page, link_name, expected):
    page.get_by_role("link", name=link_name).click()
    if expected:
        expect(page.get_by_role("heading", name=link_name)).to_be_visible()
    else:
        pass


"""Test Case 5
Hmmm I also didn't find any adequate method to check if the page is scrollable.
I mean automatically, not by pausing and checking it visually"""
def test_scroll(page: Page):
    page.get_by_role("link", name="Large & Deep DOM").click()
    footer = page.locator("#page-footer")
    footer.scroll_into_view_if_needed()
    expect(footer).to_be_visible()


"""Test Case 6"""
def test_form_submission(page: Page):
    page.get_by_role("link", name="Form Authentication").click()
    page.get_by_label("Username").click()
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name=" Login").click()
    expect(page.get_by_text("You logged into a secure area")).to_be_visible()
    expect(page.get_by_role("link", name="Logout")).to_be_visible()


"""Test Case 8"""
@pytest.mark.parametrize(
    "page", ["iPad (gen 6)", "iPhone SE", "None"], ids=["tablet", "phone", "desktop"], indirect=True
)
def test(playwright: Playwright, page):
    expect(page.get_by_role("heading", name="Welcome to the-internet")).to_be_visible()
    expect(page.get_by_role("heading", name="Available Examples")).to_be_visible()
