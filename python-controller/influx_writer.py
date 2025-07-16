from influxdb import InfluxDBClient
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

client = InfluxDBClient(host='influxdb', port=8086, database='blockchain_anomalies')

def write_anomaly_to_influx(txid, r, s, block_height, entropy_r, entropy_s, timestamp):
    json_body = [
        {
            "measurement": "signatures",
            "tags": {
                "txid": txid,
                "block": block_height
            },
            "time": timestamp or datetime.utcnow().isoformat(),
            "fields": {
                "r": float(r),
                "s": float(s),
                "entropy_r": entropy_r,
                "entropy_s": entropy_s
            }
        }
    ]
    try:
        client.write_points(json_body)
        logging.info(f"Saved anomaly {txid} to InfluxDB")
    except Exception as e:
        logging.error(f"Failed to write to InfluxDB: {e}")