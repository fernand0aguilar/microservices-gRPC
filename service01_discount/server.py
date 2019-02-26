# !/usr/bin/python

import grpc
import os, sys
from concurrent import futures

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

        DATE_FORMAT = "%d/%m"
        BLACK_FRIDAY = datetime(2019, 11, 25).strftime(DATE_FORMAT)
        today = datetime.now().strftime(DATE_FORMAT)
        user_aniversary = user_aniversary.strftime(DATE_FORMAT)

        # print("BLACK_FRIDAY: " + BLACK_FRIDAY )
        # print("TODAY: " + today)
        # print("ANIVERSARY: " + user_aniversary)

        MAX_DISCOUNT = decimal.Decimal(10) / 100    # 10%
        percentual = 0

        if today == BLACK_FRIDAY:
            percentual = decimal.Decimal(10) / 100  # 10%
        elif today == user_aniversary:
            percentual = decimal.Decimal(5) / 100   # 5%

        percentual = 0.1 if percentual > MAX_DISCOUNT else percentual
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

def get_server(host):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    keys_dir = os.path.abspath(os.path.join('keys/', os.pardir, 'keys'))
    print(keys_dir)
    with open('%s/private.key' % keys_dir, 'rb') as f:
        private_key = f.read()

    with open('%s/cert.pem' % keys_dir, 'rb') as f:
        certificate_chain = f.read()

    if private_key and certificate_chain:
        server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))
        server.add_secure_port(host, server_credentials)

    hashtest_pb2_grpc.add_DiscountServicer_to_server(Hashtest(), server)
    return server

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 443
    host = 'localhost:%s' % port
    server = get_server(host)

    try:
        server.start()
        print('The Running Discount Service on port %s' % host)
        while True:
            time.sleep(1)
    except Exception as err:
        print('[error] %s' %err)
        server.stop(0)
