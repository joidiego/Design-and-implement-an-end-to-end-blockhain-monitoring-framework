import logging
from datetime import datetime
from influx_writer import write_anomaly_to_influx
from ml_model import OnlineAnomalyModel

logging.basicConfig(level=logging.INFO)

# Inisialisasi model
model = OnlineAnomalyModel()

def process_anomaly(anomaly):
    r = anomaly.signature.r
    s = anomaly.signature.s
    txid = anomaly.signature.txid
    block_height = anomaly.signature.block_height
    timestamp = anomaly.timestamp or datetime.utcnow().isoformat()

    # Tambahkan ke model untuk pelatihan
    model.add_data_point(r, s)

    # Deteksi apakah ini anomali
    if model.predict(r, s):
        logging.info(f"ML Anomaly Detected: TXID={txid}, r={r}, s={s}")
        write_anomaly_to_influx(
            txid=txid,
            r=r,
            s=s,
            block_height=block_height,
            entropy_r=anomaly.entropy_r,
            entropy_s=anomaly.entropy_s,
            timestamp=timestamp
        )