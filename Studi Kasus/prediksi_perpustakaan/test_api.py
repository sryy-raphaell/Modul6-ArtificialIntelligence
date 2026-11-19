"""
File: test_api.py
Deskripsi Studi Kasus:
    Sistem Informasi Perpustakaan - Prediksi Kemungkinan Keterlambatan Pengembalian Buku.
    Skrip pengujian otomatis untuk memverifikasi komunikasi antara klien dan REST API
    serta memastikan hasil prediksi tersimpan ke dalam basis data log SQLite.
Komponen Terkait:
    - Pengujian End-to-End (requests & sqlite3): Mengirimkan beberapa skenario kasus uji
      melalui HTTP POST ke '/predict' dan membaca kembali tabel 'log_peminjaman' pada
      database 'log_perpustakaan.db'.
"""

import requests
import sqlite3

URL_API = "http://localhost:5000/predict"

# Skenario pengujian dengan variasi profil anggota perpustakaan
test_cases = [
    {
        "jumlah_buku": 1,
        "rata_lama_pinjam": 3.0,
        "jenis_anggota": 0,
    },  # Mahasiswa rajin -> Tepat Waktu
    {
        "jumlah_buku": 6,
        "rata_lama_pinjam": 14.5,
        "jenis_anggota": 0,
    },  # Mahasiswa pinjam banyak & lama -> Berisiko Terlambat
    {
        "jumlah_buku": 2,
        "rata_lama_pinjam": 5.0,
        "jenis_anggota": 1,
    },  # Dosen -> Tepat Waktu
    {
        "jumlah_buku": 5,
        "rata_lama_pinjam": 13.0,
        "jenis_anggota": 2,
    },  # Anggota Umum -> Berisiko Terlambat
]

print("=== 1. MENGUJI ENDPOINT REST API ===")
for idx, kasus in enumerate(test_cases, start=1):
    res = requests.post(URL_API, json=kasus)
    print(
        f"Kasus {idx}: Input={kasus} -> Status={res.status_code}, Output={res.json()}"
    )

print("\n=== 2. VERIFIKASI DATA LAYER (SQLITE LOG) ===")
conn = sqlite3.connect("log_perpustakaan.db")
cursor = conn.cursor()
cursor.execute(
    "SELECT id, waktu, jumlah_buku, rata_lama_pinjam, jenis_anggota, label, probabilitas FROM log_peminjaman"
)
rows = cursor.fetchall()
conn.close()

print(f"Total baris tercatat di database: {len(rows)}")
for row in rows[-len(test_cases) :]:
    print(row)
