"""
File: app.py
Deskripsi Studi Kasus:
    Sistem Informasi Perpustakaan - Prediksi Kemungkinan Keterlambatan Pengembalian Buku.
    Menyediakan layanan prediksi berbasis web/API agar sistem sirkulasi perpustakaan
    dapat mendeteksi risiko keterlambatan saat transaksi peminjaman berlangsung.
Komponen Terkait:
    - API Layer (Flask): Menyediakan endpoint '/' untuk antarmuka dan '/predict' (POST)
      untuk menerima input JSON serta mengembalikan hasil prediksi JSON.
    - Model Layer (joblib): Memuat file 'model_keterlambatan.joblib' satu kali saat
      server dinyalakan (Fase Serving).
    - Data Layer (SQLite3): Menyimpan log setiap permintaan dan hasil prediksi ke dalam
      database 'log_perpustakaan.db' untuk keperluan audit dan statistik bulanan.
"""

from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 1. DATA LAYER: Inisialisasi dan fungsi pencatatan log ke SQLite
DB_NAME = "log_perpustakaan.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS log_peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT NOT NULL,
            bulan_tahun TEXT NOT NULL,
            jumlah_buku INTEGER NOT NULL,
            rata_lama_pinjam REAL NOT NULL,
            jenis_anggota INTEGER NOT NULL,
            prediksi INTEGER NOT NULL,
            label TEXT NOT NULL,
            probabilitas REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def log_prediction(data, prediksi, label, probabilitas):
    sekarang = datetime.now()
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        INSERT INTO log_peminjaman (
            waktu, bulan_tahun, jumlah_buku, rata_lama_pinjam,
            jenis_anggota, prediksi, label, probabilitas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sekarang.isoformat(),
            sekarang.strftime("%Y-%m"),
            data["jumlah_buku"],
            data["rata_lama_pinjam"],
            data["jenis_anggota"],
            prediksi,
            label,
            probabilitas,
        ),
    )
    conn.commit()
    conn.close()


# Jalankan inisialisasi tabel saat aplikasi dimulai
init_db()

# 2. MODEL LAYER: Memuat model terlatih sekali saat server aktif
model = joblib.load("model_keterlambatan.joblib")


# 3. API LAYER: Routing halaman utama dan endpoint prediksi
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Payload JSON tidak ditemukan"}), 400

    try:
        jumlah_buku = int(data["jumlah_buku"])
        rata_lama_pinjam = float(data["rata_lama_pinjam"])
        jenis_anggota = int(data["jenis_anggota"])

        if jenis_anggota not in [0, 1, 2]:
            return (
                jsonify(
                    {
                        "error": "jenis_anggota harus 0 (Mahasiswa), 1 (Dosen), atau 2 (Umum)"
                    }
                ),
                400,
            )

        fitur = np.array([[jumlah_buku, rata_lama_pinjam, jenis_anggota]])
    except KeyError as e:
        return jsonify({"error": f"Field wajib hilang: {e}"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Tipe data input tidak valid"}), 400

    # Inferensi model
    prediksi = int(model.predict(fitur)[0])
    probabilitas = float(model.predict_proba(fitur)[0][prediksi])
    label = "Berisiko Terlambat" if prediksi == 1 else "Tepat Waktu"

    # Simpan riwayat ke Data Layer
    log_prediction(
        {
            "jumlah_buku": jumlah_buku,
            "rata_lama_pinjam": rata_lama_pinjam,
            "jenis_anggota": jenis_anggota,
        },
        prediksi,
        label,
        round(probabilitas, 3),
    )

    return jsonify(
        {
            "prediksi": prediksi,
            "label": label,
            "probabilitas": round(probabilitas, 3),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
