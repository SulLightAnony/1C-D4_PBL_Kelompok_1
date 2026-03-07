# General News Scraper

General News Scraper adalah aplikasi desktop berbasis Python yang digunakan untuk mengambil (scraping) data berita dari sebuah situs berita secara otomatis. Aplikasi ini menyediakan antarmuka grafis (GUI) yang memudahkan pengguna untuk mengambil artikel berita, memfilter berdasarkan tanggal, serta mengekspor hasil scraping ke dalam format CSV atau Excel.

Aplikasi ini dibuat menggunakan library **PyQt5** untuk antarmuka, serta **Selenium WebDriver** untuk melakukan scraping halaman web secara otomatis.

---

# Fitur Utama

1. Scraping berita dari situs berita tertentu
2. Filter berita berdasarkan rentang tanggal
3. Menentukan jumlah berita yang ingin diambil
4. Progress bar untuk melihat proses scraping
5. Melihat isi konten berita langsung di aplikasi
6. Membuka artikel asli di browser
7. Export data ke:
  - CSV
  - Excel (.xlsx)
8. Tema tampilan:
  - Dark Mode
  - Light Mode

---

# Teknologi yang Digunakan

- Python
- PyQt5 (GUI Framework)
- Selenium (Web Automation)
- WebDriver Manager
- Dateparser
- Openpyxl (Export Excel)

---

## Panduan Instalasi

Pastikan Anda sudah menginstall Python (versi 3.8+) di perangkat Anda.

1.  **Clone Repository**
    ```bash
    git clone https://github.com/SulLightAnony/1C-D4_PBL_Kelompok_1.git
    cd 1C-D4_PBL_Kelompok_1
    ```

2.  **Install Dependencies**
    ```bash
    pip install PyQt5 selenium webdriver-manager dateparser openpyxl
    ```

---

## Cara Menjalankan Aplikasi

1.  **Eksekusi Program**: Jalankan file utama dengan perintah:
    ```bash
    python main.py
    ```
2.  **Konfigurasi Scraping**:
    * Masukkan **URL Website** berita (contoh: `detik.com`, `kompas.com`).
    * Input **Jumlah Berita** yang ingin diambil.
    * Atur **Rentang Tanggal** melalui widget kalender/filter yang tersedia.
3.  **Proses**: Klik tombol **"Mulai Scraping"** dan tunggu hingga progress selesai.
4.  **Interaksi Hasil**:
    * **Lihat Konten**: Membuka modal internal untuk membaca teks berita.
    * **Buka URL**: Mengarahkan langsung ke sumber berita di browser.
5.  **Penyimpanan**: Pilih opsi **Export CSV** atau **Export Excel** untuk menyimpan data.

---

## Struktur Proyek

| File | Deskripsi |
| :--- | :--- |
| `main.py` | **Entry Point**: Inisialisasi dan menjalankan siklus hidup aplikasi. |
| `gui.py` | **User Interface**: Mengatur layout, widget, dan interaksi pengguna (PyQt5). |
| `scraper.py` | **Core Engine**: Logika otomasi browser menggunakan Selenium. |
| `theme.py` | **Styling**: Konfigurasi skema warna Dark Mode dan Light Mode. |

---

## Preview Tampilan

### Tampilan Utama
![Tampilan Utama](preview/tampilan-utama.png)


---

## Kontributor
**Kelompok C1 - D4 Teknik Informatika**
---

## Lisensi & Catatan
Project ini dikembangkan untuk keperluan 
**pembelajaran dan tugas akademik (PBL)**. Dilarang menyalahgunakan alat ini untuk aktivitas yang melanggar kebijakan *terms of service* dari situs berita terkait.
