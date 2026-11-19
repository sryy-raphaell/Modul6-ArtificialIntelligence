"""
File: train_model.py
Deskripsi Studi Kasus:
    Sistem Informasi Kesehatan Kampus - Klasifikasi Tingkat Risiko Stres Mahasiswa.
    Mengklasifikasikan kondisi risiko stres mahasiswa ke dalam 3 kelas
    (0 = Rendah, 1 = Sedang, 2 = Tinggi) berdasarkan data kuesioner harian.
Komponen Terkait:
    - Model Layer (Fase Training): Menggunakan scikit-learn (MLPClassifier) untuk
      klasifikasi multi-kelas dan joblib untuk serialisasi model ke file .joblib.
    - Fitur Input: [jam_tidur, beban_sks, jam_kerja_paruh_waktu]
"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Dataset historis hasil kuesioner kesehatan mahasiswa
# Fitur: [jam_tidur_per_hari, beban_sks_semester, jam_kerja_paruh_waktu_per_minggu]
X = np.array(
    [
        [8.0, 18, 0],  # Tidur cukup, SKS normal, tidak kerja -> Risiko Rendah (0)
        [7.5, 20, 4],  # Tidur cukup, SKS normal, kerja ringan -> Risiko Rendah (0)
        [8.5, 16, 0],  # Istirahat sangat baik -> Risiko Rendah (0)
        [7.0, 19, 5],  # Pola seimbang -> Risiko Rendah (0)
        [6.0, 22, 10,],  # Tidur agak kurang, SKS padat, kerja paruh waktu -> Risiko Sedang (1)
        [5.5, 20, 12],  # Tidur kurang, beban kerja sedang -> Risiko Sedang (1)
        [6.5, 24, 8],  # SKS maksimal, tidur cukup -> Risiko Sedang (1)
        [6.0, 21, 14],  # Tekanan waktu mulai tinggi -> Risiko Sedang (1)
        [4.0, 24, 20,],  # Kurang tidur parah, SKS penuh, kerja berat -> Risiko Tinggi (2)
        [4.5, 22, 25],  # Kelelahan fisik & akademik -> Risiko Tinggi (2)
        [3.5, 24, 18],  # Defisit tidur ekstrem -> Risiko Tinggi (2)
        [5.0, 23, 22],  # Beban ganda berat -> Risiko Tinggi (2)
    ]
)

# Label Target: 0 = Risiko Rendah, 1 = Risiko Sedang, 2 = Risiko Tinggi
y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])

# Membagi data latih dan data uji (75% latih, 25% uji) dengan stratifikasi kelas
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Menggunakan Pipeline (StandardScaler + MLPClassifier)
model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(10, 6), activation="relu", max_iter=2500, random_state=42
    ),
)

# Melatih model
model.fit(X_train, y_train)

# Evaluasi akurasi pada data uji
akurasi = model.score(X_test, y_test)
print(f"Akurasi model pada data uji: {akurasi:.2f}")

# Serialisasi model ke file fisik untuk digunakan oleh API Layer
nama_file_model = "model_stres.joblib"
joblib.dump(model, nama_file_model)
print(f"Model berhasil disimpan sebagai '{nama_file_model}'")
