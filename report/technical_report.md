# Laporan Teknis: Deteksi Anomali Tanda Tangan ECDSA

## Metodologi
- Ekstraksi `r, s` dari transaksi mentah via ZeroMQ
- Perhitungan entropi rolling dan bias nonce
- Threshold 6% dari baseline historis
- Model Isolation Forest untuk adaptasi

## Deteksi Serangan
- **Nonce reuse**: `r` sama → `s` berbeda → kunci privat bisa dihitung
- **Side-channel**: distribusi `r/s` tidak acak → bocoran RNG
- **Kunci lemah**: entropi rendah → rentan brute-force

## Hasil
- Sistem mendeteksi anomali dalam waktu <1 detik
- Akurasi ditingkatkan oleh model online
- Data tersedia real-time via API