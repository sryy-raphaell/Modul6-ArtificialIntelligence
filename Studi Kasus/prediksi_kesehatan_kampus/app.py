"""
File: app.py
Deskripsi Studi Kasus:
    Sistem Informasi Kesehatan Kampus - Klasifikasi Tingkat Risiko Stres Mahasiswa.
    Menyediakan layanan prediksi REST API agar sistem portal kesehatan mahasiswa dapat
    memberikan rekomendasi konseling otomatis berdasarkan hasil kuesioner.
Komponen Terkait:
    - API Layer (Flask): Menyediakan endpoint '/' untuk antarmuka dan '/predict' (POST)
      untuk menerima input JSON kuesioner serta mengembalikan hasil klasifikasi JSON.
    - Model Layer (joblib): Memuat file 'model_stres.joblib' satu kali saat server aktif.
    - Data Layer (SQLite3): Menyimpan log riwayat skrining stres ke database 'log_kesehatan.db'
      untuk pemantauan tren kesehatan mental mahasiswa per bulan/semester.
"""

from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Pemetaan label kelas stres
LABEL_STRES = {
    0: "Risiko Stres Rendah",
    1: "Risiko Stres Sedang",
    2: "Risiko Stres Tinggi",
}

# 1. DATA LAYER: Inisialisasi dan pencatatan log ke SQLite
DB_NAME = "log_kesehatan.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS log_stres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT NOT NULL,
            bulan_tahun TEXT NOT NULL,
            jam_tidur REAL NOT NULL,
            beban_sks INTEGER NOT NULL,
            jam_kerja_paruh_waktu REAL NOT NULL,
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
        INSERT INTO log_stres (
            waktu, bulan_tahun, jam_tidur, beban_sks,
            jam_kerja_paruh_waktu, prediksi, label, probabilitas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sekarang.isoformat(),
            sekarang.strftime("%Y-%m"),
            data["jam_tidur"],
            data["beban_sks"],
            data["jam_kerja_paruh_waktu"],
            prediksi,
            label,
            probabilitas,
        ),
    )
    conn.commit()
    conn.close()


init_db()

# 2. MODEL LAYER: Memuat model terlatih sekali saat server dijalankan
model = joblib.load("model_stres.joblib")


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
        jam_tidur = float(data["jam_tidur"])
        beban_sks = int(data["beban_sks"])
        jam_kerja = float(data["jam_kerja_paruh_waktu"])

        if not (0 <= jam_tidur <= 24) or beban_sks < 0 or jam_kerja < 0:
            return jsonify({"error": "Nilai input berada di luar batas wajar"}), 400

        fitur = np.array([[jam_tidur, beban_sks, jam_kerja]])
    except KeyError as e:
        return jsonify({"error": f"Field wajib hilang: {e}"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Tipe data input tidak valid"}), 400

    # Inferensi multi-kelas
    prediksi = int(model.predict(fitur)[0])
    probabilitas = float(model.predict_proba(fitur)[0][prediksi])
    label = LABEL_STRES.get(prediksi, "Tidak Diketahui")

    # Simpan riwayat ke Data Layer
    log_prediction(
        {
            "jam_tidur": jam_tidur,
            "beban_sks": beban_sks,
            "jam_kerja_paruh_waktu": jam_kerja,
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
