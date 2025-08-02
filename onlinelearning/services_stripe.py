import logging

import stripe
from django.conf import settings

logger = logging.getLogger(__name__)

# Инициализация Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.max_network_retries = 2


class StripeService:

    @classmethod
    def _check_keys(cls):
        """Проверка наличия ключей"""
        if not stripe.api_key:
            raise ValueError("Stripe secret key is not configured")
        if not settings.STRIPE_PUBLIC_KEY:
            raise ValueError("Stripe public key is not configured")

    @staticmethod
    def create_product(name: str, description: str = "") -> str:
        """Создает продукт в Stripe"""
        StripeService._check_keys()

        try:
            logger.info(f"Creating product: {name}")
            product = stripe.Product.create(
                name=name,
                description=description,
                metadata={"service": "online-learning"},
            )
            logger.info(f"Product created: {product.id}")
            return product.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise

    @staticmethod
    def create_price(amount: float, product_id: str, currency: str = "rub") -> str:
        """Создает цену для продукта"""
        StripeService._check_keys()

        try:
            logger.info(f"Creating price for product {product_id}")
            price = stripe.Price.create(
                unit_amount=int(amount * 100),
                currency=currency,
                product=product_id,
            )
            logger.info(f"Price created: {price.id}")
            return price.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise

    @staticmethod
    def create_checkout_session(
        price_id: str, success_url: str, cancel_url: str
    ) -> dict:
        """Создает сессию оплаты"""
        StripeService._check_keys()

        try:
            logger.info(f"Creating checkout session for price {price_id}")
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            logger.info(f"Session created: {session.id}")
            return {"session_id": session.id, "payment_url": session.url}
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise
