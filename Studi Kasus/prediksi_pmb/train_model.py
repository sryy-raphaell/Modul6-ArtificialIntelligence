"""
File: train_model.py
Deskripsi Studi Kasus:
    Sistem Informasi Penerimaan Mahasiswa Baru (PMB) - Prediksi Kemungkinan Lolos Seleksi.
    Memprediksi status kelulusan calon mahasiswa (1 = Lolos Seleksi, 0 = Tidak Lolos)
    berdasarkan komponen penilaian akademik dan non-akademik.
Komponen Terkait:
    - Model Layer (Fase Training): Menggunakan scikit-learn (MLPClassifier + StandardScaler)
      untuk melatih jaringan syaraf tiruan dan joblib untuk serialisasi ke file .joblib.
    - Fitur Input: [nilai_rapor, skor_tes, nilai_wawancara] (skala 0 - 100)
"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Dataset historis pendaftar PMB tahun-tahun sebelumnya
# Fitur: [nilai_rapor, skor_tes_tertulis, nilai_wawancara] (skala 0 - 100)
X = np.array(
    [
        [88.5, 85.0, 90.0],  # Semua komponen tinggi -> Lolos (1)
        [91.0, 82.0, 86.0],  # Rapor unggul, tes & wawancara baik -> Lolos (1)
        [65.0, 60.0, 68.0],  # Semua komponen rendah -> Tidak Lolos (0)
        [70.0, 58.0, 62.0],  # Skor tes rendah -> Tidak Lolos (0)
        [84.0, 80.0, 82.0],  # Konsisten di atas ambang batas -> Lolos (1)
        [62.0, 64.0, 55.0],  # Wawancara & rapor rendah -> Tidak Lolos (0)
        [89.0, 88.0, 85.0],  # Kandidat kuat -> Lolos (1)
        [72.0, 65.0, 60.0],  # Belum memenuhi standar -> Tidak Lolos (0)
        [82.0, 79.0, 84.0],  # Wawancara kuat menopang nilai cukup -> Lolos (1)
        [68.0, 62.0, 65.0],  # Rata-rata di bawah standar -> Tidak Lolos (0)
        [93.0, 90.0, 88.0],  # Kandidat sangat unggul -> Lolos (1)
        [74.0, 61.0, 64.0],  # Skor tes & wawancara kurang -> Tidak Lolos (0)
    ]
)

# Label Target: 0 = Tidak Lolos Seleksi, 1 = Lolos Seleksi
y = np.array([1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0])

# Membagi data latih dan data uji (75% latih, 25% uji) dengan stratifikasi kelas
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Menggunakan Pipeline (StandardScaler + MLPClassifier)
model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(8, 4), activation="relu", max_iter=2000, random_state=42
    ),
)

# Melatih model
model.fit(X_train, y_train)

# Evaluasi akurasi pada data uji
akurasi = model.score(X_test, y_test)
print(f"Akurasi model pada data uji: {akurasi:.2f}")

# Serialisasi model ke file fisik untuk fase serving
nama_file_model = "model_seleksi_pmb.joblib"
joblib.dump(model, nama_file_model)
print(f"Model berhasil disimpan sebagai '{nama_file_model}'")
