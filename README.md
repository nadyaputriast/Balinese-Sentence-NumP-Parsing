# Balinese Sentence NumP Parsing

Sebuah sistem *parser* sintaksis kalimat Bahasa Bali yang berfokus pada pengenalan dan validasi **Frasa Numeralia (NumP)**. Proyek ini dibangun menggunakan pendekatan *Context-Free Grammar* (CFG) dan mengimplementasikan algoritma CYK (*Cocke-Younger-Kasami*) untuk menganalisis struktur kalimat dan menghasilkan pohon *parse* (*parse tree*) secara otomatis.

Proyek ini juga menyertakan basis data leksikon (kamus) Bahasa Bali yang komprehensif untuk mendukung pemetaan kategori kelas kata (Part-of-Speech) secara dinamis.

## ✨ Fitur Utama
- **Validasi Kalimat:** Memeriksa kebenaran struktur tata bahasa kalimat Bahasa Bali berdasarkan aturan CFG yang telah didefinisikan.
- **CYK Parser:** Implementasi algoritma CYK murni dengan dukungan konversi otomatis tata bahasa ke dalam bentuk *Chomsky Normal Form* (CNF).
- **Pembersihan Grammar:** Deteksi dan penghapusan *epsilon production* serta *unit production* secara otomatis pada sistem.
- **Visualisasi Parse Tree:** Menghasilkan representasi visual berupa grafik pohon sintaksis untuk kalimat yang dinyatakan valid.
- **Batch Processing:** Mendukung pemrosesan data massal dengan mengunggah file dokumen (CSV, XLSX, DOCX, TXT) untuk memvalidasi banyak kalimat sekaligus.

## 📂 Struktur Proyek
- `app.py` — *Entrypoint* aplikasi antarmuka berbasis Streamlit.
- `core/` — Implementasi mesin utama (`cnf_converter.py`, `cyk_parser.py`, `parse_tree_generator.py`).
- `grammar/` — Aturan dasar tata bahasa (CFG) dan modul pemetaan leksikon (`cfg_rules.py`).
- `scraping/` — Modul ekstraksi data otomatis (`build_knowledge_base.py`) untuk membangun *knowledge base*.
- `ui/` — Komponen antarmuka pengguna dan *styling* CSS (`app_ui.py`, `styles.py`).
- `utils/` — Skrip utilitas pendukung seperti pemrosesan *batch* dan manajemen statistik.
- `balinese_lexicon.json` — Berkas basis data leksikon yang digunakan oleh sistem.

## 🚀 Instalasi & Penggunaan

**1. Persiapan Lingkungan**
Sangat disarankan untuk menjalankan aplikasi ini di dalam *virtual environment*:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**2. Pemasangan Dependensi**

```bash
pip install -r requirements.txt
```

(Catatan: Jika ada variabel lingkungan yang diperlukan, silakan salin `.env.example` menjadi `.env` dan sesuaikan isinya.)

**3. Menjalankan Aplikasi**

```bash
streamlit run app.py
```

Akses UI Streamlit melalui browser lokal Anda. Masukkan kalimat Bahasa Bali pada form yang tersedia, lalu sistem akan menampilkan status validasi, tabel parse, dan gambar parse tree (jika valid).

## ⚠️ Atribusi Data & Leksikon (Data Disclaimer)
Kamus leksikon (`balinese_lexicon.json`) yang digunakan dalam proyek ini dikumpulkan menggunakan metode automated retrieval dari sumber data leksikal terbuka (Glosbe).

Data mentah tersebut telah melalui tahap pembersihan dan validasi manual secara mendalam—khususnya pada entri kelas kata bilangan (Numeralia) dan penggolongnya—untuk memastikan akurasi pada sistem parsing ini.

### Pernyataan Penggunaan (Fair Use)

Data leksikon di dalam repositori ini disediakan semata-mata untuk keperluan penelitian, akademik, dan edukasi.

Kami tidak mengklaim hak cipta atau kepemilikan atas data mentah leksikon tersebut. Data diperlakukan sebagai aset pihak ketiga.

Dilarang mendistribusikan ulang atau menggunakan data leksikon ini untuk kepentingan komersial tanpa merujuk dan mematuhi ketentuan lisensi dari pemilik sumber data asli.

## 💬 Kontak & Kontribusi
Pull request sangat kami terima. Untuk penambahan fitur besar atau laporan bug, silakan buka Issue terlebih dahulu agar dapat didiskusikan.

Jika ada pertanyaan terkait penelitian ini, jangan ragu untuk menghubungi melalui tab Issues pada repositori ini.