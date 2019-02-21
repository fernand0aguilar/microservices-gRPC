import sys, os
import datetime
import decimal
import hashtest_pb2, hashtest_pb2_grpc
# b'\x03\xf3\r\n'
class Hashtest(hashtest_pb2_grpc.DiscountServicer):
    def apply_discount(self, request, content):
        product = request.product
        discount = hashtest_pb2.DiscountValue()
        user = request.user

        # TODO -> Find better way to calculate percentages
        percentual = calculate_discount(user)
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

        def calculate_discount(user):
            DATE_FORMAT = "%d/%m"
            BLACK_FRIDAY = datetime.datetime(2019, 11, 25).strftime(DATE_FORMAT)
            today = datetime.datetime.now().strftime(DATE_FORMAT)
            user_aniversary = user.date_of_birth.strftime(DATE_FORMAT)
            
            MAX_DISCOUNT = decimal.Decimal(10) / 100    # 10%
            percentual = 0
            
            if today == BLACK_FRIDAY:
                percentual = decimal.Decimal(10) / 100  # 10%
            elif today == user_aniversary:
                percentual = decimal.Decimal(5) / 100   # 5%

            percentual = 0.1 if percentual > MAX_DISCOUNT else percentual
            
            return percentual