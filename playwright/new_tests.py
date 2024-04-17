import pytest
from playwright.sync_api import Page, expect

URL = "https://magento.softwaretestingboard.com"

@pytest.fixture(scope="function")
def page(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)
    page.get_by_label("Consent", exact=True).click()
    yield page
    context.close()
    browser.close()

def test_register_customer(page: Page):
    page.click("text=Create an Account")
    expect(page).to_have_url(f"{URL}/customer/account/create/")
    page.fill("input[name='firstname']", "John")
    page.fill("input[name='lastname']", "Doe")
    page.fill("input[name='email']", "johndoe@example.com")
    page.fill("input[name='password']", "Password1")
    page.fill("input[name='password_confirmation']", "Password1")
    submit_button_xpath = "/html/body/div[2]/main/div[3]/div/form/div/div[1]/button"
    page.click(f"xpath={submit_button_xpath}")

    expect(page.locator("text=There is already an account")).to_be_visible()

def test_add_to_cart_options_not_selected(page: Page):
    page.click("text=What's New")
    page.click("text=Phoebe Zipper Sweatshirt")
    page.click("text=Add to Cart")

    size_error_locator = page.locator("[id='super_attribute[143]-error']")
    color_error_locator = page.locator("[id='super_attribute[93]-error']")
    
    expect(size_error_locator).to_have_text("This is a required field.")
    expect(color_error_locator).to_have_text("This is a required field.")

def test_add_to_cart_options_selected(page: Page):
    page.click("text=What's New")
    page.click("text=Phoebe Zipper Sweatshirt")
    page.locator("text=XS").click()
    gray_color_selector = "div.swatch-option.color[option-label='Gray'][option-id='52']"
    page.locator(gray_color_selector).click()
    page.click("text=Add to Cart")
    page.wait_for_timeout(2000)
    expect(page.locator("text=You added Phoebe Zipper Sweatshirt to your shopping cart")).to_be_visible()
    page.click("text=Cart")
    page.click("text=See details")
    expect(page.locator("a[data-bind*='product_url'][data-bind*='product_name']:has-text('Phoebe Zipper Sweatshirt')")).to_be_visible()
    expect(page.locator("dl.product.options.list >> text=Size >> xpath=following-sibling::dd >> text=XS")).to_be_visible()
    expect(page.locator("dl.product.options.list >> text=Color >> xpath=following-sibling::dd >> text=Gray")).to_be_visible()

def test_complete_purchase_workflow(page: Page):
    page.click("text=Cart")
    expect(page.locator("text=You have no items in your shopping cart")).to_be_visible()
    page.click("text=Radiant Tee")
    page.locator("text=XL").click()
    orange_color_selector = "div.swatch-option.color[option-label='Orange'][option-id='56']"
    page.locator(orange_color_selector).click()
    page.click("text=Add to Cart")
    page.wait_for_timeout(2000)
    expect(page.locator("text=You added Radiant Tee to your shopping cart")).to_be_visible()
    page.click("text=Cart")
    page.click("text=Proceed to Checkout")
    page.wait_for_timeout(2000)
    expect(page.locator("text=Shipping Address")).to_be_visible()
    expect(page.locator("text=Order Summary")).to_be_visible()

    page.click("text=Next")
    expect(page.locator("text=The shipping method is missing")).to_be_visible()
    page.get_by_label("Fixed").check()
    page.click("text=Next")

    email_selector = "input#customer-email"
    page.wait_for_selector(email_selector)
    expect(page.locator("text=This is a required field")).to_have_count(8)  # Example check

    # Fill the form
    page.fill(email_selector, "johndoe@example.com")
    page.fill("input[name='firstname']", "John")
    page.fill("input[name='lastname']", "Doe")
    page.fill("input[name='street[0]']", "123 Elm Street")
    page.fill("input[name='city']", "Metropolis")
    page.select_option("select[name='region_id']", "1")
    page.fill("input[name='postcode']", "12345")
    page.fill("input[name='telephone']", "1234567890")

    # Proceed to payment and confirmation
    page.click("text=Next")
    page.wait_for_timeout(2000)
    expect(page).to_have_url("https://magento.softwaretestingboard.com/checkout/#payment")

    # Verify that the "Place Order" button is present and correctly configured
    place_order_button_selector = "button.action.primary.checkout[type='submit']"
    expect(page.locator(place_order_button_selector)).to_be_visible()
    expect(page.locator(place_order_button_selector)).to_have_attribute("title", "Place Order")
