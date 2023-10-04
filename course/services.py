import os
import stripe

from rest_framework import serializers
from course.models import Course, Payment


def get_session_of_payment(self):
    stripe.api_key = os.getenv('STRIPE_KEY')
    amount = self.request.data.get('amount')
    paid_course_id = self.request.data.get('course')
    payment_course = Course.objects.get(pk=paid_course_id)

    if payment_course:
        stripe_product = stripe.Product.create(name=payment_course.title)
        stripe_price = stripe.Price.create(
            unit_amount=amount,
            currency='usd',
            product=stripe_product.stripe_id,
        )

    return stripe.checkout.Session.create(
            success_url='https://example.com/success',
            line_items=[
                {
                    "price": stripe_price.stripe_id,
                    "quantity": 1,
                },
            ],
            mode='payment',
        )


def save_serializer(self, session, serializer: serializers) -> None:
    serializer.save(
        stripe_id=session.get('id'),
        stripe_url=session.get('url'),
        stripe_status=session.get('status'),
        user=self.request.user,
        method=Payment.TRANSFER,
    )


def get_payment_data(stripe_id) -> None:
    stripe.api_key = os.getenv('STRIPE_KEY')
    return stripe.checkout.Session.retrieve(stripe_id)


