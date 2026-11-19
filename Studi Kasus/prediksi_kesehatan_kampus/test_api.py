"""
File: test_api.py
Deskripsi Studi Kasus:
    Sistem Informasi Kesehatan Kampus - Klasifikasi Tingkat Risiko Stres Mahasiswa.
    Skrip pengujian end-to-end untuk memvalidasi endpoint klasifikasi multi-kelas
    serta memverifikasi pencatatan riwayat kuesioner pada database SQLite.
Komponen Terkait:
    - Pengujian End-to-End (requests & sqlite3): Mengirimkan 3 skenario profil mahasiswa
      (risiko rendah, sedang, tinggi) ke '/predict' dan memeriksa isi tabel 'log_stres'.
"""

import requests
import sqlite3

URL_API = "http://localhost:5000/predict"

# Skenario pengujian untuk ketiga kelas tingkat stres
test_cases = [
    {"jam_tidur": 8.0, "beban_sks": 18, "jam_kerja_paruh_waktu": 0},  # Risiko Rendah
    {"jam_tidur": 6.0, "beban_sks": 22, "jam_kerja_paruh_waktu": 10},  # Risiko Sedang
    {"jam_tidur": 4.0, "beban_sks": 24, "jam_kerja_paruh_waktu": 20},  # Risiko Tinggi
]

print("=== 1. MENGUJI ENDPOINT REST API ===")
for idx, kasus in enumerate(test_cases, start=1):
    res = requests.post(URL_API, json=kasus)
    print(
        f"Kasus {idx}: Input={kasus} -> Status={res.status_code}, Output={res.json()}"
    )

print("\n=== 2. VERIFIKASI DATA LAYER (SQLITE LOG) ===")
conn = sqlite3.connect("log_kesehatan.db")
cursor = conn.cursor()
cursor.execute(
    "SELECT id, waktu, jam_tidur, beban_sks, jam_kerja_paruh_waktu, label, probabilitas FROM log_stres"
)
rows = cursor.fetchall()
conn.close()

print(f"Total baris tercatat di database: {len(rows)}")
for row in rows[-len(test_cases) :]:
    print(row)
