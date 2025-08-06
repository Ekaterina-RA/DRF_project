import logging

import stripe
from django.conf import settings

logger = logging.getLogger(__name__)


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.max_network_retries = 2


class StripeService:

    @classmethod
    def _check_keys(cls):
        """Проверяем наличие ключей"""
        if not stripe.api_key:
            raise ValueError("Stripe secret key не подключен")
        if not settings.STRIPE_PUBLIC_KEY:
            raise ValueError("Stripe public key не подключен")

    @staticmethod
    def create_product(name, description):
        """Создаем продукт в Stripe"""
        StripeService._check_keys()

        try:
            logger.info(f"Создаем товар: {name}")
            product = stripe.Product.create(
                name=name,
                description=description,
                metadata={"service": "online-learning"},
            )
            logger.info(f"Товар создан: {product.id}")
            return product.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise

    @staticmethod
    def create_price(amount, product_id, currency="rub"):
        """Создаем стоимость товара"""
        StripeService._check_keys()

        try:
            logger.info(f"Создание стоимости для товара {product_id}")
            price = stripe.Price.create(
                unit_amount=int(amount * 100),
                currency=currency,
                product=product_id,
            )
            logger.info(f"Стоимость создана: {price.id}")
            return price.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise

    @staticmethod
    def create_session(price_id, success_url, cancel_url):
        """Создаем сессию оплаты"""
        StripeService._check_keys()

        try:
            logger.info(f"Создание сессии для оплаты {price_id}")
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
            logger.info(f"Сессия создана: {session.id}")
            return {"session_id": session.id, "payment_url": session.url}
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise
