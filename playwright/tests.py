import pytest
from playwright.sync_api import Playwright, Page, expect


URL = "https://magento.softwaretestingboard.com/"
USER_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@mail.com",
    "password": "Password1",
    "street": "Street",
    "city": "LA",
    "zip": "00000",
    "phone": "800000000"

}


@pytest.fixture
def open_page(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


def fill_field(page: Page, field_name: str, value: str) -> None:
    page.get_by_label(field_name, exact=True).click()
    page.get_by_label(field_name, exact=True).fill(value)


def test_register_customer(open_page: Page) -> None:
    open_page.goto(URL)
    open_page.get_by_role("link", name="Create an Account").click()
    expect(open_page.get_by_text("Create New Customer Account")).to_be_visible()
    name, last_name = USER_DATA["first_name"], USER_DATA["last_name"]
    fill_field(page = open_page, field_name= "First Name", value = name)
    fill_field(page=open_page, field_name="Last Name", value=last_name)
    fill_field(page=open_page, field_name="Email", value=USER_DATA["email"])
    fill_field(page=open_page, field_name="Password", value=USER_DATA["password"])
    fill_field(page=open_page, field_name="Confirm Password", value=USER_DATA["password"])
    open_page.get_by_role("button", name="Create an Account").click()
    if open_page.get_by_role("alert").is_visible(timeout=5000): #I can't find working locator
        open_page.get_by_role("link", name="click here").click()
        expect(open_page.get_by_role("heading", name="Forgot Your Password?").locator("span")).to_be_visible()
    else:
        expect(open_page.get_by_text(f"Welcome, {name} {last_name}!")).to_be_visible()
        expect(open_page.get_by_role("heading", name="My Account").locator("span")).to_be_visible()


def test_add_to_cart_options_not_selected(open_page: Page) -> None:
    open_page.goto(URL)
    open_page.get_by_role("menuitem", name="What's New").click()
    open_page.locator("li").filter(has_text="Phoebe Zipper Sweatshirt As").get_by_role("button").click()
    expect(open_page.get_by_role("heading", name="Phoebe Zipper Sweatshirt").locator("span")).to_be_visible()


def test_add_to_cart_options_selected(open_page: Page) -> None:
    open_page.goto(URL)
    open_page.get_by_role("menuitem", name="What's New").click()
    open_page.locator("li").filter(has_text="Phoebe Zipper Sweatshirt As").get_by_label("XS").click()
    open_page.get_by_label("Gray").click()
    open_page.locator("li").filter(has_text="Phoebe Zipper Sweatshirt As").get_by_role("button").click()
    open_page.get_by_role("link", name=" My Cart 1 1\nitems").click()
    expect(open_page.locator("#mini-cart").get_by_text("Phoebe Zipper Sweatshirt")).to_be_visible()


def test_place_an_order(open_page: Page) -> None:
    open_page.goto(URL)
    open_page.get_by_role("link", name="Radiant Tee").first.click()
    open_page.get_by_label("Blue").click()
    open_page.get_by_label("XS").click()
    open_page.get_by_role("button", name="Add to Cart").click()
    expect(open_page.get_by_role("alert")).to_be_visible()
    open_page.locator("xpath=/html/body/div[2]/header/div[2]/div[1]/a/span[2]").click()
    button = open_page.get_by_role("button", name="Proceed to Checkout")
    expect(button).to_be_visible()
    button.click()
    fill_field(page=open_page, field_name="First Name", value=USER_DATA["first_name"])
    fill_field(page=open_page, field_name="Last Name", value=USER_DATA["last_name"])
    fill_field(page=open_page, field_name="Email Address *", value=USER_DATA["email"])
    address = open_page.locator('xpath=//*[@id="shipping-new-address-form"]/fieldset/div/div[1]/div') #there is an issue with this locator
    address.click()
    address.fill(USER_DATA["street"])
    fill_field(page=open_page, field_name="Zip/Postal Code", value=USER_DATA["zip"])
    fill_field(page=open_page, field_name="City", value=USER_DATA["city"])
    fill_field(page=open_page, field_name="Phone Number", value=USER_DATA["phone"])
    open_page.locator("select[name=\"region_id\"]").select_option("1")
    open_page.locator("#checkout-step-shipping").click()
    open_page.get_by_label("Fixed").check()
    open_page.get_by_role("button", name="Next").click()
    expect(open_page.get_by_text("Review & Payments")).to_be_visible()
    expect(open_page.locator("span").filter(has_text="Order Summary")).to_be_visible()
    expect(open_page.get_by_role("rowgroup").get_by_text("Flat Rate - Fixed")).to_be_visible()
    expect(open_page.get_by_role("row", name="Order Total $").locator("span")).to_be_visible()
