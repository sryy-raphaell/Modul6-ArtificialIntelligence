# Materi & Panduan Presentasi: Integrasi Teknik AI dalam Sistem Informasi

Dokumen ini memuat rangkuman materi inti dari **Modul 6: Integrasi Teknik AI dalam Sistem Informasi**, struktur *slide* presentasi (PPT), serta naskah penjelasan mendetail untuk penyampaian di kelas.

---

## Bagian 1: Ringkasan Materi Sebelum Studi Kasus

### 1. Konteks & Capaian Modul
- Modul ini menjembatani pembuatan model murni (Perceptron/MLP) menuju penerapannya di dalam sistem informasi fungsional.
- Mahasiswa diharapkan mampu melatih model, menyimpannya ke file, membungkusnya menjadi layanan **REST API**, mencatat riwayat prediksi ke basis data, serta mengujinya secara *end-to-end*.

### 2. Sistem Informasi Konvensional vs. Berbasis AI
| Aspek | Sistem Informasi Konvensional | Sistem Informasi Berbasis AI |
| :--- | :--- | :--- |
| **Basis Logika** | Aturan bisnis eksplisit (*hardcoded* `if-else`) | Pola yang dipelajari dari data historis |
| **Pembaruan** | Memerlukan perubahan kode program manual | Cukup melatih ulang model dengan data baru |
| **Sifat Output** | Deterministik berdasarkan kondisi tetap | Prediktif disertai nilai probabilitas |

### 3. Tiga Prinsip Utama Integrasi AI
1. **Decoupling (Pemisahan):** Model AI dipisahkan dari kode aplikasi utama agar pembaruan model tidak merusak kode antarmuka maupun logika aplikasi.
2. **Model as a Service (MaaS):** Model disajikan melalui antarmuka standar (**REST API**) agar dapat diakses lintas platform (Web, Mobile, Desktop) secara agnostik.
3. **Pemisahan Siklus Hidup (Training vs. Serving):**
   - **Fase Training:** Dilakukan *offline* dan berkala; membutuhkan komputasi besar untuk mencari bobot optimal.
   - **Fase Serving:** Dilakukan *real-time* (online) setiap ada permintaan masuk; harus ringan dan cepat.

### 4. Arsitektur Berlapis (*Layered Architecture*)
1. **Application Layer:** Antarmuka pengguna (HTML/JS) pengirim input dan penampil hasil.
2. **API Layer:** Endpoint REST (Flask) penerima *request* JSON dan pengirim *response* JSON.
3. **Model Layer:** File model terlatih yang dimuat sekali saat server aktif untuk melakukan inferensi.
4. **Data Layer:** Basis data (SQLite3) penyimpan riwayat permintaan dan hasil prediksi untuk audit.

**Alur Kerja Sistem:**
$$\text{Pengguna} \rightarrow \text{HTTP Request (JSON)} \rightarrow \text{API Layer} \rightarrow \text{Model Layer} \rightarrow \text{Data Layer} \rightarrow \text{HTTP Response (JSON)} \rightarrow \text{Pengguna}$$

### 5. Serialisasi Model & Tech Stack
- **Serialisasi (`.joblib` / `.pkl`):** Membekukan bobot dan parameter model hasil latihan ke file fisik sebagai penghubung antara fase *training* dan *serving* tanpa perlu melatih ulang model saat server dinyalakan.
- **Tech Stack:** `scikit-learn` (pelatihan ANN), `joblib` (serialisasi), `Flask` (REST API), `SQLite3` (basis data log), dan `requests` (pengujian *end-to-end*).

---

## Bagian 2: Struktur Slide PPT & Naskah Presentasi

### Slide 1: Judul Presentasi
- **Isi Slide:** Mata Kuliah Artificial Intelligence — *Integrasi Teknik AI dalam Sistem Informasi: Landasan Konsep, Prinsip, dan Arsitektur Sebelum Implementasi Studi Kasus*.
- **Naskah Penyampaian:**
  > "Selamat pagi/siang semuanya. Pada kesempatan ini, kita akan membahas Modul 6 mengenai Integrasi Teknik AI dalam Sistem Informasi. Sebelum kita masuk ke baris kode dan studi kasus, kita akan membedah terlebih dahulu fondasi arsitektur bagaimana sebuah model kecerdasan buatan bisa digunakan secara nyata di dalam aplikasi."

### Slide 2: Konteks & Tujuan Modul
- **Isi Slide:** Jembatan implementasi, penyajian layanan REST API, pencatatan riwayat database, dan pengujian *end-to-end*.
- **Naskah Penyampaian:**
  > "Pada modul sebelumnya, kita sudah membangun model Jaringan Syaraf Tiruan seperti MLP. Namun, model yang hanya berjalan di notebook belum bisa diakses oleh pengguna umum. Fokus modul ini adalah membungkus model terlatih tersebut menjadi layanan mandiri yang terhubung dengan database dan antarmuka pengguna."

### Slide 3: Sistem Konvensional vs. Sistem AI
- **Isi Slide:** Perbandingan aturan eksplisit (kaku, deterministik) dengan pembelajaran pola data (adaptif, prediktif).
- **Naskah Penyampaian:**
  > "Sistem konvensional bekerja menggunakan aturan `if-else` yang ditulis manual oleh programmer. Jika kebijakan berubah, kode harus diubah. Dengan mengintegrasikan AI, sistem mengambil keputusan berdasarkan pola data historis, sehingga pembaruan cukup dilakukan dengan melatih ulang model tanpa membongkar kode aplikasi utama."

### Slide 4 & 5: Tiga Prinsip Integrasi & Siklus Hidup (Training vs. Serving)
- **Isi Slide:** *Decoupling*, *Model as a Service*, dan pemisahan fase *Training* (offline, berat) vs. *Serving* (online, cepat).
- **Naskah Penyampaian:**
  > "Ada tiga prinsip arsitektur utama: pertama *Decoupling* atau pemisahan kode model dan aplikasi; kedua *Model as a Service* menggunakan REST API agar bisa diakses klien web maupun mobile; dan ketiga pemisahan siklus hidup antara fase *training* yang berat secara *offline* dengan fase *serving* yang cepat secara *real-time*."

### Slide 6 & 7: Arsitektur Berlapis & Alur Permintaan Data
- **Isi Slide:** Tabel 4 lapisan (*Application, API, Model, Data*) dan diagram alur 5 langkah dari pengguna hingga respons kembali.
- **Naskah Penyampaian:**
  > "Sistem dibagi menjadi empat lapisan tanggung jawab. Saat pengguna menekan tombol prediksi di *Application Layer*, data dikirim dalam format JSON ke *API Layer* (Flask), diteruskan ke *Model Layer* untuk dihitung prediksinya, dicatat ke *Data Layer* (SQLite), lalu dikembalikan sebagai respons JSON ke layar pengguna."

### Slide 8 & 9: Konsep Serialisasi Model & Tech Stack
- **Isi Slide:** Format `.joblib`/`.pkl` tanpa latih ulang serta peran `scikit-learn`, `joblib`, `Flask`, dan `SQLite3`.
- **Naskah Penyampaian:**
  > "Penghubung antara fase *training* dan *serving* adalah serialisasi model. Objek model yang sudah dilatih disimpan menjadi file `.joblib`, lalu dimuat satu kali oleh server Flask saat dijalankan sehingga server tidak perlu melatih ulang model dari nol."

---

## Bagian 3: Pembahasan Jawaban Pertanyaan Latihan Mandiri (Slide 10–14)

### 1. Fitur Input Model & Relevansinya (Slide 11)
- **Studi Kasus 1 (Sistem Informasi Perpustakaan):** Menggunakan `jumlah_buku`, `rata_lama_pinjam`, dan `jenis_anggota`. Relevan karena mengukur beban bacaan, kebiasaan disiplin pengembalian historis, serta perbedaan kebijakan batas pinjam antar kategori anggota.
- **Studi Kasus 2 (Sistem Informasi Kesehatan Kampus):** Menggunakan `jam_tidur`, `beban_sks`, dan `jam_kerja_paruh_waktu`. Relevan karena memetakan kelelahan fisiologis, intensitas tekanan akademik, dan potensi beban ganda (*role overload*).
- **Studi Kasus 3 (Sistem Informasi Penerimaan Mahasiswa Baru):** Menggunakan `nilai_rapor`, `skor_tes`, dan `nilai_wawancara`. Relevan karena mengombinasikan konsistensi akademik jangka panjang, kemampuan kognitif terstandar, dan kesiapan non-kognitif.

### 2. Perancangan Skema Tabel Log untuk Analisis Lanjutan (Slide 12)
- **`id` & `waktu` (ISO-8601):** Menjamin keunikan baris transaksi dan memudahkan pengurutan kronologis (*time-series*).
- **`bulan_tahun` (`YYYY-MM`):** Mempercepat kueri agregasi statistik bulanan menggunakan klausa `GROUP BY bulan_tahun` tanpa perlu melakukan *parsing string* tanggal berulang kali.
- **Kolom Fitur Input:** Disimpan mentah untuk mendeteksi pergeseran distribusi data (*data drift*) serta menjadi bahan dataset *retraining* model di masa mendatang.
- **Kolom Output (`prediksi`, `label`, `probabilitas`):** Memudahkan perhitungan rasio kelas per bulan serta pemantauan tingkat keyakinan (*confidence*) model.

### 3. Risiko Jika API Model Tidak Tersedia (*Down*) & Solusinya (Slide 13)
- **Risiko:** Transaksi pada sistem informasi utama gagal total (*error/timeout*) jika pemanggilan API dilakukan secara sinkron, antarmuka pengguna menjadi macet (*hang*), dan riwayat log prediksi tidak tercatat selama gangguan.
- **Mitigasi Teknis:**
  1. **Graceful Degradation (Fallback):** Membungkus pemanggilan API dengan batas waktu singkat (`timeout`) dan beralih otomatis ke aturan statis sederhana jika API gagal merespons.
  2. **Antrean Asinkron (*Retry Queue*):** Menyimpan transaksi utama terlebih dahulu ke database, lalu menjalankan prediksi di latar belakang saat layanan API kembali pulih.
  3. **Process Manager & Health Check:** Menggunakan *process manager* (`systemd`, Supervisor, atau Docker) disertai endpoint `/health` agar server otomatis melakukan *restart* saat terjadi *crash*.