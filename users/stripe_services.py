import stripe
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course_name, description=''):
    try:
        product = stripe.Product.create(
            name=course_name,
            description=description,
            type='service',
        )
        return product.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка создания продукта: {e.user_message}")

def create_stripe_price(product_id, payment_amount):
    try:
        amount_in_cents = int(Decimal(payment_amount) * 100)
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount_in_cents,
            currency='rub',
        )
        return price.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка создания цены: {e.user_message}")

def create_stripe_session(price_id, success_url, cancel_url, user_email):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=user_email,
        )
        return session.id, session.url
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка создания сессии: {e.user_message}")

def get_payment_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка проверки статуса: {e.user_message}")
