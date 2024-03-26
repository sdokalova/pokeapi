This directory contains tests written with Playwright and Pytest for https://magento.softwaretestingboard.com/

Test cases:

Test Case 1
1. go to Create an Account
2. fill form
3. submit

ER: If email was not used before - successful account registration
else - warning

Test Case 2
1. go to What’s new
2. select Phoebe Zipper Sweatshirt
3. click Add to cart

ER: Phoebe Zipper Sweatshirt page is opened with warning You need to choose options for your item.

Test Case 3
1. go to What’s new
2. select Phoebe Zipper Sweatshirt
3. pick XS size and Gray color
4. click Add to cart
5. You added Phoebe Zipper Sweatshirt to your shopping cart message is shown
6. click on Cart
7. click on See details

ER:  Phoebe Zipper Sweatshirt is in the cart in selected size and color

Test Case 4
1. click Cart
ER: You have no items in your shopping cart is shown,
2. click on Gobi HeatTec® Tee
3. pick XL red
4. click Add to Cart
5. click Cart
6. click Proceed to Checkout
ER: Shipping Address form is shown, selected item is in Order Summary
7. click Next
ER: You need to select shipping method warning is shown
8. select Shipping method
9. click Next
10. there are warnings for obligatory fields
11. fill form

ER: page with payment and order confirmation