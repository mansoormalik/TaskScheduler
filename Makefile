all:
	@sh grpc.sh

clean:
	@rm -rf __pycache__ masterslave_pb2_grpc.py masterslave_pb2.py *~
