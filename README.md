# Modul 6: Integrasi Teknik AI dalam Sistem Informasi

Repositori ini berisi implementasi praktikum, materi presentasi, dan tugas mandiri mata kuliah **Artificial Intelligence** terkait integrasi model _Artificial Neural Network_ (ANN) ke dalam sistem informasi fungsional menggunakan arsitektur layanan (_Model as a Service_).

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

## Arsitektur & Struktur Direktori

Setiap studi kasus dibangun menggunakan pendekatan arsitektur berlapis (_Layered Architecture_):

- **Application Layer (`templates/index.html`):** Antarmuka web berbasis HTML/JavaScript untuk mengirim input dan menampilkan hasil prediksi.
- **API Layer (`app.py`):** Endpoint REST (`/predict`) berbasis Flask yang memvalidasi payload JSON dan mengembalikan respons prediksi.
- **Model Layer (`train_model.py` & `*.joblib`):** Model `MLPClassifier` (`scikit-learn`) yang telah dilatih dan diserialisasi.
- **Data Layer (`*.db`):** Basis data SQLite3 untuk menyimpan log transaksi prediksi dan audit statistik.

```text
Modul6-ArtificialIntelligence/
├── .gitignore
├── README.md
├── Materi/
│   └── MATERI.md                                     # Rangkuman teori, naskah PPT & pembahasan latihan
├── Laporan/                                          # Versi Jupyter Notebook (All-in-One per kasus)
│   ├── Kasus1/
│   │   └── Studi_Kasus_1_Perpustakaan.ipynb
│   ├── Kasus2/
│   │   └── Studi_Kasus_2_Kesehatan_Kampus.ipynb
│   └── Kasus3/
│       └── Studi_Kasus_3_PMB.ipynb
└── Studi Kasus/                                      # Versi Modular Python Scripts
    ├── prediksi_perpustakaan/                        # Studi Kasus 1: Risiko Keterlambatan Buku
    │   ├── train_model.py
    │   ├── app.py
    │   ├── test_api.py
    │   └── templates/index.html
    ├── prediksi_kesehatan_kampus/                    # Studi Kasus 2: Klasifikasi Risiko Stres Mahasiswa
    │   ├── train_model.py
    │   ├── app.py
    │   ├── test_api.py
    │   └── templates/index.html
    └── prediksi_pmb/                                 # Studi Kasus 3: Prediksi Kelulusan Seleksi PMB
        ├── train_model.py
        ├── app.py
        ├── test_api.py
        └── templates/index.html
```

---

## Prasyarat & Cara Menjalankan Proyek

### 1. Clone Repositori & Instalasi Pustaka

```bash
git clone https://github.com/sryy-raphaell/Modul6-ArtificialIntelligence.git
cd Modul6-ArtificialIntelligence
pip install scikit-learn joblib flask requests numpy
```

---

### 2. Opsi A — Menjalankan Versi Modular Python (`Studi Kasus/`)

Pilih salah satu folder studi kasus (misalnya `prediksi_perpustakaan`, `prediksi_kesehatan_kampus`, atau `prediksi_pmb`):

1. **Masuk ke direktori studi kasus:**
   ```bash
   cd "Studi Kasus/prediksi_perpustakaan"
   ```
2. **Langkah 1 — Melatih & Menyimpan Model (Fase Training):**
   ```bash
   python train_model.py
   ```
   _Menghasilkan file model terlatih (`_.joblib`) secara otomatis.\*
3. **Langkah 2 — Menjalankan Server API (Fase Serving):**
   ```bash
   python app.py
   ```
   _Server aktif pada `http://localhost:5000`. Buka alamat tersebut di browser untuk mencoba antarmuka web._
4. **Langkah 3 — Pengujian End-to-End:**
   Buka terminal baru pada direktori kasus yang sama (selagi `app.py` berjalan), lalu jalankan:
   ```bash
   python test_api.py
   ```

---

### 3. Opsi B — Menjalankan Versi Jupyter Notebook (`Laporan/`)

Setiap notebook di dalam folder `Laporan/Kasus1/`, `Laporan/Kasus2/`, dan `Laporan/Kasus3/` sudah mencakup keseluruhan alur (_training_, pembuatan `templates/index.html`, server Flask, hingga pengujian _end-to-end_):

1. Buka file `.ipynb` melalui VS Code atau Jupyter Notebook.
2. Klik **Run All** untuk mengeksekusi seluruh sel secara berurutan.
3. Masing-masing notebook berjalan di _background thread_ dengan port berbeda agar tidak bentrok:
   - **Kasus 1 (Perpustakaan):** Port `5001`
   - **Kasus 2 (Kesehatan Kampus):** Port `5002`
   - **Kasus 3 (Seleksi PMB):** Port `5003`

> **Catatan Artefak Otomatis:** File model (`*.joblib`) dan database lokal (`*.db`) diabaikan oleh `.gitignore` dan akan terbentuk otomatis saat skrip pelatihan atau notebook dijalankan.

---

## Tata Cara Penggunaan GitHub

### A. Panduan untuk Anggota Tim (Kolaborasi Pengembangan)

Agar tidak terjadi konflik kode (_merge conflict_) saat bekerja secara berkelompok, ikuti alur kerja berikut:

1. **Ambil pembaruan terbaru sebelum mulai bekerja:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Buat _branch_ baru sesuai bagian tugas masing-masing:**
   ```bash
   # Contoh: fitur-kasus1, fitur-kasus2, update-materi, dll.
   git checkout -b fitur-nama-tugas
   ```
3. **Simpan perubahan secara berkala (_Commit_):**
   ```bash
   git status
   git add .
   git commit -m "feat: menambahkan pengujian end-to-end pada studi kasus"
   ```
4. **Unggah _branch_ ke GitHub (_Push_):**
   ```bash
   git push origin fitur-nama-tugas
   ```
5. **Ajukan _Pull Request_ (PR):**
   - Buka halaman repositori di GitHub: [Modul6-ArtificialIntelligence](https://github.com/sryy-raphaell/Modul6-ArtificialIntelligence)
   - Klik tombol **Compare & pull request**.
   - Tuliskan ringkasan perubahan yang dikerjakan, lalu lakukan _review_ bersama anggota tim sebelum menekan tombol **Merge pull request** ke `main`.

---

### B. Panduan untuk Dosen Pengampu / Asisten Praktikum (Evaluasi & Penilaian)

Untuk meninjau kode sumber, riwayat kontribusi anggota tim, serta menguji aplikasi:

1. **Mengunduh Proyek:**
   - Klik tombol hijau **`<> Code`** pada halaman repositori, lalu pilih **Download ZIP**, atau jalankan perintah:
     ```bash
     git clone https://github.com/sryy-raphaell/Modul6-ArtificialIntelligence.git
     ```
2. **Memeriksa Kontribusi Tiap Anggota Tim:**
   - Buka tab **Insights** $\rightarrow$ **Contributors** pada GitHub untuk melihat grafik dan statistik kontribusi setiap anggota.
   - Buka tab **Commits** atau **Pull requests** (filter: _Closed_) untuk melihat pembagian kerja dan riwayat pengerjaan secara kronologis.
3. **Membaca Materi & Menjalankan Pengujian:**
   - Rangkuman materi dan jawaban latihan mandiri tersedia di `Materi/MATERI.md`.
   - Pengujian aplikasi dapat dilakukan melalui **Opsi A** (`Studi Kasus/`) maupun **Opsi B** (`Laporan/`).
