echo "Generating py proto files"
cd service01_discount
python -m grpc_tools.protoc -I=.. --python_out=. --grpc_python_out=. ../hashtest.proto

echo "Generating go proto files"
cd ../service02_products_listing
mkdir hashtest
protoc -I=.. --go_out=plugins=grpc:hashtest ../hashtest.proto