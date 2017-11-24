run:
	@python driver.py

build:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./masterslave.proto

clean:
	@rm -rf __pycache__ masterslave_pb2_grpc.py masterslave_pb2.py *~
