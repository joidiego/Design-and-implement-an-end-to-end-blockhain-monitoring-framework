from fastapi import FastAPI
from influxdb import InfluxDBClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = InfluxDBClient(host='influxdb', port=8086, database='blockchain_anomalies')

@app.get("/anomalies")
def get_anomalies():
    result = client.query("SELECT * FROM signatures ORDER BY time DESC LIMIT 100")
    return list(result.get_points())

@app.get("/block/{height}")
def get_anomalies_by_block(height: int):
    result = client.query(f"SELECT * FROM signatures WHERE block = {height}")
    return list(result.get_points())

@app.get("/entropy")
def get_entropy():
    result = client.query("SELECT entropy_r, entropy_s FROM signatures ORDER BY time DESC LIMIT 100")
    return list(result.get_points())

@app.get("/ml/status")
def get_ml_status():
    from anomaly_analyzer import model
    return {
        "trained": model.fitted,
        "data_points": len(model.data)
    }

@app.get("/count")
def count_anomalies():
    result = client.query("SELECT COUNT(r) FROM signatures")
    points = list(result.get_points())
    return points[0] if points else {"count": 0}