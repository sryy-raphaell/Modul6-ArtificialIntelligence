"""
File: train_model.py
Deskripsi Studi Kasus:
    Sistem Informasi Perpustakaan - Prediksi Kemungkinan Keterlambatan Pengembalian Buku.
    Memprediksi apakah anggota perpustakaan berisiko terlambat mengembalikan buku (1)
    atau tepat waktu (0) berdasarkan riwayat peminjaman.
Komponen Terkait:
    - Model Layer (Fase Training): Menggunakan scikit-learn (MLPClassifier) untuk melatih
      model Artificial Neural Network dan joblib untuk serialisasi model ke file .joblib.
    - Fitur Input: [jumlah_buku, rata_lama_pinjam, jenis_anggota]
      (jenis_anggota: 0 = Mahasiswa, 1 = Dosen/Staf, 2 = Umum)
"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Dataset historis peminjaman perpustakaan
# Fitur: [jumlah_buku_dipinjam, lama_rata_rata_peminjaman_hari, jenis_anggota]
# jenis_anggota: 0 = Mahasiswa, 1 = Dosen/Staf, 2 = Umum
X = np.array(
    [
        [1, 3.0, 0],  # Pinjam sedikit, cepat kembali, mahasiswa -> Tepat waktu
        [2, 4.5, 1],  # Dosen, kembali cepat -> Tepat waktu
        [5, 12.0, 0],  # Pinjam banyak, rata-rata lama -> Terlambat
        [4, 14.5, 2],  # Umum, pinjam banyak & lama -> Terlambat
        [1, 5.0, 1],  # Dosen, pinjam 1 buku -> Tepat waktu
        [6, 15.0, 0],  # Mahasiswa, beban bacaan tinggi & lama -> Terlambat
        [2, 6.0, 2],  # Umum, cepat kembali -> Tepat waktu
        [5, 11.5, 2],  # Umum, pinjam banyak & lama -> Terlambat
        [3, 5.5, 0],  # Mahasiswa, sedang & tepat waktu -> Tepat waktu
        [4, 13.0, 1],  # Dosen, pinjam banyak & sangat lama -> Terlambat
        [2, 3.5, 0],  # Mahasiswa, cepat kembali -> Tepat waktu
        [6, 16.0, 2],  # Umum, sangat berisiko terlambat -> Terlambat
    ]
)

# Label Target: 0 = Tepat Waktu, 1 = Berisiko Terlambat
y = np.array([0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1])

# Membagi data latih dan data uji (75% latih, 25% uji)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Menggunakan Pipeline (StandardScaler + MLPClassifier) agar skala fitur seragam
# dan bobot ANN cepat konvergen
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

# Serialisasi model ke file fisik untuk digunakan oleh API Layer
nama_file_model = "model_keterlambatan.joblib"
joblib.dump(model, nama_file_model)
print(f"Model berhasil disimpan sebagai '{nama_file_model}'")
