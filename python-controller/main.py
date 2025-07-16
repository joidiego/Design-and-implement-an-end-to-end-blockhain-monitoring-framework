import grpc
from concurrent import futures
import grpc_service_pb2_grpc as pb2_grpc
import grpc_service_pb2 as pb2
import anomaly_analyzer

class AnomalyService(pb2_grpc.AnomalyServiceServicer):
    def ReportAnomaly(self, request_iterator, context):
        for anomaly in request_iterator:
            anomaly_analyzer.process_anomaly(anomaly)
        return pb2.AnomalyResponse(success=True, message="Anomalies processed")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AnomalyServiceServicer_to_server(AnomalyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Python gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()