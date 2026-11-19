# Modul 6: Integrasi Teknik AI dalam Sistem Informasi

Repositori ini berisi implementasi praktikum dan tugas mandiri mata kuliah **Artificial Intelligence** terkait integrasi model _Artificial Neural Network_ (ANN) ke dalam sistem informasi fungsional menggunakan arsitektur layanan (_Model as a Service_).

---

## Deskripsi Modul & Tujuan Praktikum

Pada modul ini, fokus pembelajaran bergeser dari sekadar melatih model _machine learning_ di lingkungan eksperimen menuju penerapan model ke dalam perangkat lunak yang siap digunakan oleh klien melalui antarmuka terstandar (**REST API**).

### Capaian Pembelajaran (Sub-CPMK):

1. Memahami konsep dan alasan pemisahan (_decoupling_) model AI dari aplikasi utama.
2. Melatih dan melakukan serialisasi model ANN agar dapat dimuat kembali tanpa pelatihan ulang.
3. Membangun REST API menggunakan **Flask** untuk menyajikan model sebagai layanan prediksi.
4. Mengintegrasikan basis data **SQLite3** untuk pencatatan riwayat (_logging_) permintaan dan hasil prediksi.
5. Menguji sistem secara _end-to-end_ mulai dari antarmuka pengguna hingga penyimpanan basis data.

---

## Arsitektur & Struktur Proyek

Sistem dibangun menggunakan pendekatan arsitektur berlapis (_Layered Architecture_):

- **Application Layer (`templates/index.html`):** Antarmuka web berbasis HTML/JavaScript untuk mengirim input dan menampilkan hasil prediksi.
- **API Layer (`app.py`):** Endpoint REST (`/predict`) berbasis Flask yang memvalidasi payload JSON dan mengembalikan respons prediksi.
- **Model Layer (`train_model.py` & `*.joblib`):** Model `MLPClassifier` (`scikit-learn`) yang telah dilatih dan diserialisasi.
- **Data Layer (`*.db`):** Basis data SQLite3 untuk menyimpan log transaksi prediksi dan audit statistik.

```text
├── README.md                 # Dokumentasi repositori & panduan GitHub
├── materi_dan_presentasi.md  # Rangkuman materi & naskah presentasi (PPT)
├── train_model.py            # Skrip pelatihan & serialisasi model (Fase Training)
├── app.py                    # Server Flask REST API & logging SQLite (Fase Serving)
├── test_api.py               # Skrip pengujian end-to-end otomatis
└── templates/
    └── index.html            # Antarmuka pengguna (Web UI)
```

---

## Prasyarat & Cara Menjalankan Proyek

1. **Clone repositori ini:**

   ```bash
   git clone https://github.com/sryy-raphaell/Modul6-ArtificialIntelligence.git
   cd "Modul 6"
   ```

2. **Instalasi pustaka (_dependencies_) Python:**
   Pastikan Python 3.8+ sudah terpasang, lalu jalankan:

   ```bash
   pip install scikit-learn joblib flask requests numpy
   ```

3. **Langkah 1 — Melatih & Menyimpan Model (Fase Training):**

   ```bash
   python train_model.py
   ```

   _Perintah ini akan menghasilkan file model terlatih berekstensi `.joblib`._

4. **Langkah 2 — Menjalankan Server API (Fase Serving):**

   ```bash
   python app.py
   ```

   _Server berjalan di `http://localhost:5000`. Buka alamat tersebut di browser untuk mengakses antarmuka web._

5. **Langkah 3 — Pengujian End-to-End:**
   Buka terminal baru (selagi `app.py` tetap berjalan), lalu jalankan:
   ```bash
   python test_api.py
   ```

---

## Tata Cara Penggunaan GitHub

### A. Panduan untuk Anggota Tim (Kolaborasi Pengembangan)

Agar tidak terjadi konflik kode (_merge conflict_) saat bekerja secara berkelompok, ikuti alur kerja berikut:

1. **Mengambil pembaruan terbaru sebelum mulai bekerja:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Membuat _branch_ baru sesuai bagian tugas masing-masing:**
   ```bash
   # Contoh: fitur-model, fitur-api, fitur-ui, atau dokumentasi
   git checkout -b fitur-nama-tugas
   ```
3. **Menyimpan perubahan secara berkala (_Commit_):**
   ```bash
   git status
   git add .
   git commit -m "feat: menambahkan validasi input pada endpoint predict"
   ```
4. **Mengunggah _branch_ ke GitHub (_Push_):**
   ```bash
   git push origin fitur-nama-tugas
   ```
5. **Mengajukan _Pull Request_ (PR):**
   - Buka halaman repositori di GitHub.
   - Klik tombol **Compare & pull request**.
   - Tuliskan deskripsi perubahan yang dilakukan, lalu minta rekan tim untuk melakukan _review_ sebelum menekan tombol **Merge pull request** ke `main`.

> **Catatan Penting (`.gitignore`):** File hasil generate otomatis seperti `__pycache__/`, lingkungan virtual (`venv/`), serta file database lokal sementara (`*.db`) sebaiknya tidak ditimpa secara sembarangan antar anggota tim.

---

### B. Panduan untuk Dosen Pengampu / Asisten Praktikum (Evaluasi & Penilaian)

Untuk meninjau kode sumber, riwayat kontribusi anggota tim, serta menguji aplikasi:

1. **Mengunduh Proyek Mahasiswa:**
   - Klik tombol hijau **`<> Code`** di bagian atas repositori, lalu pilih **Download ZIP**, atau gunakan perintah:
     ```bash
     git clone <url-repositori-ini>
     ```
2. **Memeriksa Kontribusi Tiap Anggota Tim:**
   - Buka tab **Insights** $\rightarrow$ **Contributors** pada halaman GitHub untuk melihat statistik kontribusi setiap anggota.
   - Buka menu **Commits** atau **Pull requests** (filter: _Closed_) untuk melihat pembagian tugas dan riwayat pengerjaan secara kronologis.
3. **Menjalankan & Menguji Aplikasi:**
   - Ikuti langkah pada bagian **Cara Menjalankan Proyek** di atas (`train_model.py` $\rightarrow$ `app.py` $\rightarrow$ `test_api.py`) atau periksa hasil pengujian pada file laporan PDF yang disertakan.
