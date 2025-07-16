import logging
from datetime import datetime
from influx_writer import write_anomaly_to_influx
from ml_model import OnlineAnomalyModel

logging.basicConfig(level=logging.INFO)

model = OnlineAnomalyModel()

def process_anomaly(anomaly):
    r = anomaly.signature.r
    s = anomaly.signature.s
    txid = anomaly.signature.txid
    block_height = anomaly.signature.block_height
    timestamp = anomaly.timestamp or datetime.utcnow().isoformat()

    # Tambahkan ke model
    model.add_data_point(r, s)

    # Prediksi apakah ini benar-benar anomali
    is_ml_anomaly = model.predict(r, s)

    if is_ml_anomaly:
        logging.info(f"ML Detected Anomaly: {txid}")
        write_anomaly_to_influx(
            txid=txid,
            r=r,
            s=s,
            block_height=block_height,
            entropy_r=anomaly.entropy_r,
            entropy_s=anomaly.entropy_s,
            timestamp=timestamp
        )