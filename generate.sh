echo "Generating py proto files"
cd discount
python -m grpc_tools.protoc -I=.. --python_out=. --grpc_python_out=. ../hashtest.proto

echo "Generating go proto files"
cd ../products_listing
mkdir hashtest
protoc -I=.. --go_out=plugins=grpc:hashtest ../hashtest.proto