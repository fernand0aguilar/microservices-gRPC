# !/usr/bin/python

import grpc
import os, sys, time
from concurrent import futures

from hashtest import Hashtest
import hashtest_pb2
import hashtest_pb2_grpc

def get_server(host):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    keys_dir = os.path.abspath(os.path.join('.', os.pardir, 'keys'))
    
    with open('%s/private.key' % keys_dir, 'rb') as file:
        private_key = file.read()
    with open('%s/cert.pem' % keys_dir, 'rb') as file:
        certificate_chain = file.read()

    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))
    server.add_secure_port(host, server_credentials)
    hashtest_pb2_grpc.add_DiscountServicer_to_server(Hashtest(), server)
    
    return server

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 443
    host = '[::]:%s' % port
    server = get_server(host)
    
    try:
        server.start()
        print('Running The Discount Server on port %s' % host)
        while True:
            time.sleep(1)
    except Exception as err:
        print('[error] %s' %err)
        server.stop(0)