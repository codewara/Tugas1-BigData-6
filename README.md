# Tugas 1 - Big Data

## Deskripsi
Repositori ini berisi tiga skrip Python untuk pengambilan dan penyimpanan data ke MongoDB dari berbagai sumber:
1. **Scraping Laporan Keuangan IDX** - Mengambil laporan keuangan dari situs IDX dan menyimpannya dalam MongoDB.
2. **Scraping Berita IQPlus** - Mengambil berita terbaru dari situs IQPlus dan menyimpannya ke dalam MongoDB.
3. **Pengambilan Data Saham dari Yahoo Finance** - Mengambil data saham berdasarkan ticker dari file CSV dan menyimpannya ke dalam MongoDB.

## Persyaratan
Pastikan Anda telah menginstal pustaka berikut sebelum menjalankan skrip:
```bash
pip install selenium pymongo requests xmltodict yfinance pandas
```

## Struktur Direktori
```
Tugas1-BigData-6/
│── yfinance/                # Folder yfinance
│───|── tickers.csv         # Daftar ticker saham untuk pengambilan data dari Yahoo Finance
│───|── YahooFinance.py     # Skrip untuk mengambil data saham dari Yahoo Finance
│── IDX.py                   # Skrip untuk scraping laporan keuangan IDX
│── iqplus.py                # Skrip untuk scraping berita dari IQPlus
│── README.md                # Skrip untuk mengambil data saham dari Yahoo Finance
```

## Panduan Penggunaan
### 1️⃣ Scraping Laporan Keuangan IDX
Jalankan skrip berikut untuk mengambil laporan keuangan dari IDX:
```bash
python IDX.py
```
Skrip ini akan:
- Mengakses situs IDX dan menetapkan filter tahun serta jenis laporan.
- Menavigasi antar halaman untuk mengambil semua data.
- Mengunduh file ZIP laporan keuangan dan mengekstrak data XML.
- Mengonversi data ke format JSON dan menyimpannya ke MongoDB.

### 2️⃣ Scraping Berita dari IQPlus
Jalankan skrip berikut untuk mengambil berita dari IQPlus:
```bash
python iqplus.py
```
Skrip ini akan:
- Mengakses situs IQPlus dan mengambil daftar berita terbaru.
- Mengunjungi setiap halaman berita dan mengambil isi berita.
- Menyimpan data berita ke MongoDB.

### 3️⃣ Pengambilan Data Saham dari Yahoo Finance
Pastikan Anda memiliki file `tickers.csv` berisi daftar ticker saham. Kemudian, jalankan:
```bash
python YahooFinance.py
```
Skrip ini akan:
- Membaca daftar ticker dari `tickers.csv`.
- Mengambil data harga saham dari Yahoo Finance untuk setiap ticker.
- Menyimpan data saham ke MongoDB.

## Catatan Tambahan
- Pastikan MongoDB telah berjalan di `localhost:27017`.
- Untuk scraping IDX dan IQPlus, pastikan Anda memiliki WebDriver yang sesuai dengan browser Anda.
- Untuk Yahoo Finance, pastikan `tickers.csv` berisi ticker yang benar.

## Lisensi
Proyek ini bersifat open-source dan bebas digunakan untuk keperluan akademik maupun penelitian.