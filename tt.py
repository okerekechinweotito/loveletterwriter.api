"""
  this is a reference file, please dont delete. thanks
"""

# import stripe
# from dotenv import load_dotenv
# import os 
# load_dotenv()


# stripe.api_key = os.getenv("STRIPE_API_KEY")


# cus = stripe.Customer.create(email="ed@gmg.com")

# sub = stripe.Subscription.create(
#     customer=cus.id,
#     items =[
#         {
#             'plan':'price_1MAWaQGYYMC7FKsIArbh4GrR'
#         }
#     ],
#     payment_behavior="default_incomplete",
#     payment_settings={"save_default_payment_method": "on_subscription"},
#     expand=["latest_invoice.payment_intent"]
# )

# chc = stripe.billing_portal.Session.create(
#     customer = cus.id,
#     return_url ="http://example.com"
# )

# print(chc.url)





# import stripe

# # Set your secret key: remember to change this to your live secret key in production
# # See your keys here: https://dashboard.stripe.com/account/apikeys
# stripe.api_key = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'

# # Get the customer ID
# customer_id = 'cus_4fdAW5ftNQow1a'

# # Get the subscription to be cancelled
# subscription = stripe.Subscription.retrieve(customer_id)

# # Check if the subscription is already cancelled
# if subscription.status == 'cancelled':
#   print('Subscription is already cancelled')
# else:
#   # Check if the subscription has expired
#   if subscription.status == 'active' and subscription.current_period_end < current_time:
#     # Cancel the subscription
#     subscription.delete()
#     print('Subscription has been cancelled')
#   else:
#     print('Subscription is still active or has not yet expired')

# import stripe

# # Set your secret key: remember to change this to your live secret key in production
# # See your keys here: https://dashboard.stripe.com/account/apikeys
# stripe.api_key = 'sk_test_your_api_key'

# # Create a customer
# customer = stripe.Customer.create(
#   email='customer@example.com',
# )

# # Create a subscription
# subscription = stripe.Subscription.create(
#   customer=customer.id,
#   items=[
#     {
#       'plan': 'plan_your_plan_id',
#     },
#   ]
# )

# # Generate a checkout link
# checkout_link = stripe.BillingPortal.Session.create(
#   customer=customer.id,
#   return_url='https://example.com/success',
# )

# print(checkout_link.url)

# import stripe

# # Set your secret key: remember to change this to your live secret key in production
# # See your keys here: https://dashboard.stripe.com/account/apikeys
# stripe.api_key = "sk_test_1234567890"

# # Get the subscription to check
# subscription_id = "sub_1234567890"
# subscription = stripe.Subscription.retrieve(subscription_id)

# # Check the subscription's expiration date
# if subscription.current_period_end < datetime.now().timestamp():
#     # The subscription has expired, so update the customer's details

#     # Get the customer associated with the subscription
#     customer_id = subscription.customer
#     customer = stripe.Customer.retrieve(customer_id)

#     # Update the customer's details
#     customer.name = "John Doe"
#     customer.email = "johndoe@example.com"
#     customer.save()