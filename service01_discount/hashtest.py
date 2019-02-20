import sys, os
import datetime
import decimal
import hashtest_pb2, hashtest_pb2_grpc


class Hashtest(hashtest_pb2_grpc.DiscountServicer):
    def ApplyDiscount(self, request, content):
        # TODO -> Refactor discount validation to another function

        DATE_FORMAT = "%d/%m"
        BLACK_FRIDAY = datetime.datetime(2019, 11, 25).strftime(DATE_FORMAT)
        MAX_DISCOUNT = decimal.Decimal(10) / 100  # 10%

        user = request.user
        product = request.product
        discount = hashtest_pb2.DiscountValue()

        # REFACTOR
        today = datetime.datetime.now().strftime(DATE_FORMAT)
        user_aniversary = user.date_of_birth.strftime(DATE_FORMAT)

        if today == BLACK_FRIDAY:
            percentual = decimal.Decimal(10) / 100  # 10%
        elif today == user_aniversary:
            percentual = decimal.Decimal(5) / 100  # 5%

        percentual = 0.1 if percentual > MAX_DISCOUNT else percentual
        # END

        # TODO -> Find better way to calculate percentages
        price = decimal.Decimal(product.price_in_cents) / 100
        new_price = price - (price * percentual)
        value_in_cents = int(new_price * 100)
        discount = hashtest_pb2.DiscountValue(
            pct=percentual, value_in_cents=value_in_cents)

        new_product = hashtest_pb2.Product(
            id=product.id,
            price_in_cents=product.price_in_cents,
            title=product.title,
            description=product.description,
            discount=discount)

        return hashtest_pb2.DiscountResponse(product=new_product)