"""
File: test_api.py
Deskripsi Studi Kasus:
    Sistem Informasi Penerimaan Mahasiswa Baru (PMB) - Prediksi Kemungkinan Lolos Seleksi.
    Skrip pengujian end-to-end untuk menguji respons REST API pada berbagai profil pendaftar
    serta memverifikasi pencatatan log ke dalam database SQLite.
Komponen Terkait:
    - Pengujian End-to-End (requests & sqlite3): Mengirimkan skenario pengujian melalui
      HTTP POST ke '/predict' dan memverifikasi tabel 'log_seleksi' pada 'log_pmb.db'.
"""

import requests
import sqlite3

URL_API = "http://localhost:5000/predict"

# Skenario pengujian profil calon mahasiswa
test_cases = [
    {
        "nilai_rapor": 90.0,
        "skor_tes": 86.0,
        "nilai_wawancara": 88.0,
    },  # Kandidat kuat -> Lolos
    {
        "nilai_rapor": 64.0,
        "skor_tes": 59.0,
        "nilai_wawancara": 61.0,
    },  # Nilai rendah -> Tidak Lolos
    {
        "nilai_rapor": 83.0,
        "skor_tes": 80.0,
        "nilai_wawancara": 85.0,
    },  # Kandidat kompetitif -> Lolos
    {
        "nilai_rapor": 71.0,
        "skor_tes": 63.0,
        "nilai_wawancara": 60.0,
    },  # Di bawah ambang -> Tidak Lolos
]

print("=== 1. MENGUJI ENDPOINT REST API ===")
for idx, kasus in enumerate(test_cases, start=1):
    res = requests.post(URL_API, json=kasus)
    print(
        f"Kasus {idx}: Input={kasus} -> Status={res.status_code}, Output={res.json()}"
    )

print("\n=== 2. VERIFIKASI DATA LAYER (SQLITE LOG) ===")
conn = sqlite3.connect("log_pmb.db")
cursor = conn.cursor()
cursor.execute(
    "SELECT id, waktu, nilai_rapor, skor_tes, nilai_wawancara, label, probabilitas FROM log_seleksi"
)
rows = cursor.fetchall()
conn.close()

print(f"Total baris tercatat di database: {len(rows)}")
for row in rows[-len(test_cases) :]:
    print(row)
