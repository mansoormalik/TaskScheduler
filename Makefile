run:
	@python driver.py

docker:
	@sh docker_build.sh

build:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./masterslave.proto

clean:
	@rm -rf __pycache__ masterslave_pb2_grpc.py masterslave_pb2.py *~
