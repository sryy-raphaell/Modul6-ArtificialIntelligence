"""
File: app.py
Deskripsi Studi Kasus:
    Sistem Informasi Penerimaan Mahasiswa Baru (PMB) - Prediksi Kemungkinan Lolos Seleksi.
    Menyediakan layanan prediksi berbasis REST API yang dapat diintegrasikan ke dalam
    portal pendaftaran mahasiswa baru untuk memberikan estimasi hasil seleksi.
Komponen Terkait:
    - API Layer (Flask): Menyediakan endpoint '/' untuk antarmuka web dan '/predict' (POST)
      untuk menerima data nilai pendaftar berformat JSON serta mengembalikan hasil JSON.
    - Model Layer (joblib): Memuat file 'model_seleksi_pmb.joblib' satu kali saat server aktif.
    - Data Layer (SQLite3): Mencatat riwayat evaluasi nilai pendaftar ke 'log_pmb.db'
      untuk audit panitia seleksi dan analisis tren pendaftar per periode.
"""

from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 1. DATA LAYER: Inisialisasi dan pencatatan log ke SQLite
DB_NAME = "log_pmb.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS log_seleksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT NOT NULL,
            bulan_tahun TEXT NOT NULL,
            nilai_rapor REAL NOT NULL,
            skor_tes REAL NOT NULL,
            nilai_wawancara REAL NOT NULL,
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
        INSERT INTO log_seleksi (
            waktu, bulan_tahun, nilai_rapor, skor_tes,
            nilai_wawancara, prediksi, label, probabilitas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sekarang.isoformat(),
            sekarang.strftime("%Y-%m"),
            data["nilai_rapor"],
            data["skor_tes"],
            data["nilai_wawancara"],
            prediksi,
            label,
            probabilitas,
        ),
    )
    conn.commit()
    conn.close()


init_db()

# 2. MODEL LAYER: Memuat model terlatih sekali saat server dijalankan
model = joblib.load("model_seleksi_pmb.joblib")


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
        nilai_rapor = float(data["nilai_rapor"])
        skor_tes = float(data["skor_tes"])
        nilai_wawancara = float(data["nilai_wawancara"])

        # Validasi rentang nilai 0 - 100
        for nama, nilai in [
            ("nilai_rapor", nilai_rapor),
            ("skor_tes", skor_tes),
            ("nilai_wawancara", nilai_wawancara),
        ]:
            if not (0 <= nilai <= 100):
                return (
                    jsonify({"error": f"{nama} harus berada pada rentang 0 - 100"}),
                    400,
                )

        fitur = np.array([[nilai_rapor, skor_tes, nilai_wawancara]])
    except KeyError as e:
        return jsonify({"error": f"Field wajib hilang: {e}"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Tipe data input harus berupa angka"}), 400

    # Inferensi model
    prediksi = int(model.predict(fitur)[0])
    probabilitas = float(model.predict_proba(fitur)[0][prediksi])
    label = "Lolos Seleksi" if prediksi == 1 else "Tidak Lolos Seleksi"

    # Simpan riwayat ke Data Layer
    log_prediction(
        {
            "nilai_rapor": nilai_rapor,
            "skor_tes": skor_tes,
            "nilai_wawancara": nilai_wawancara,
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
