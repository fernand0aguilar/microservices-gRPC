import sys

import time
from datetime import datetime
import decimal

import hashtest_pb2
import hashtest_pb2_grpc


class Hashtest(hashtest_pb2_grpc.DiscountServicer):
    def ApplyDiscount(self, request, content):
        product = request.product
        user = request.user
        discount = hashtest_pb2.DiscountValue()
        user_aniversary = datetime.strptime(user.date_of_birth, "%d%m%Y")

        discount_percentual = self.calculate_percentual(user_aniversary)

        price = decimal.Decimal(product.price_in_cents) / 100
        new_price = price - (price * discount_percentual)
        value_in_cents = int(new_price * 100)
        discount = hashtest_pb2.DiscountValue(
            pct=discount_percentual, value_in_cents=value_in_cents)

        new_product = hashtest_pb2.Product(
            id=product.id,
            price_in_cents=product.price_in_cents,
            title=product.title,
            description=product.description,
            discount=discount)

        return hashtest_pb2.DiscountResponse(product=new_product)

    def calculate_percentual(self, user_aniversary):
        percentual = 0
        DATE_FORMAT = "%d/%m"
        
        today = datetime.now().strftime(DATE_FORMAT)
        BLACK_FRIDAY = datetime(2019, 11, 25).strftime(DATE_FORMAT)
        user_aniversary_formated = user_aniversary.strftime(DATE_FORMAT)

        if today == BLACK_FRIDAY:
            percentual = decimal.Decimal(10) / 100  # 10%
        elif today == user_aniversary_formated:
            percentual = decimal.Decimal(5) / 100  # 5%

        MAX_DISCOUNT = decimal.Decimal(10) / 100  # 10%
        percentual = 0.1 if percentual > MAX_DISCOUNT else percentual
        
        return percentual