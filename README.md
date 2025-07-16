# Blockchain Monitoring System

Proyek ini adalah sistem pemantau blockchain end-to-end yang mendeteksi anomali dalam tanda tangan ECDSA pada transaksi Bitcoin.

## Fitur Utama:
- Subscriber ZeroMQ ke node Bitcoin Core
- Parsing tanda tangan ECDSA (r, s)
- Deteksi anomali berbasis entropi
- Penyimpanan ke InfluxDB
- REST API dengan FastAPI
- Orkestrasi Docker

## Setup:
```bash