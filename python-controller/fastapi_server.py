from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from influxdb import InfluxDBClient

app = FastAPI()

# Setup template dan static file
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Koneksi InfluxDB
client = InfluxDBClient(host='influxdb', port=8086, database='blockchain_anomalies')

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/anomalies")
def get_anomalies():
    result = client.query("SELECT * FROM signatures ORDER BY time DESC LIMIT 100")
    points = list(result.get_points())
    return [{"txid": p["txid"], "r": p["r"], "s": p["s"], "block": p["block"], "time": p["time"], "entropy_r": p["entropy_r"], "entropy_s": p["entropy_s"]} for p in points]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})