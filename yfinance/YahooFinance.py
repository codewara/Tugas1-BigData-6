import yfinance as yf
import pymongo
import time
import pandas as pd

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bigdata"]
yfinance_collection = db["yfinance"]  # Koleksi tempat menyimpan data saham dari yfinance

# Baca daftar ticker dari CSV
csv_file = "tickers.csv"  # Pastikan file ini ada di direktori yang sama dengan script
try:
    tickers_df = pd.read_csv(csv_file, header=None)  # Baca CSV tanpa header
    tickers_list = tickers_df[0].tolist()  # Konversi ke list
except Exception as e:
    print(f"ERROR: Gagal membaca CSV {csv_file}: {e}")
    exit()

if not tickers_list:
    print("ERROR: Tidak ada ticker yang ditemukan di CSV.")
    exit()

print(f"Ditemukan {len(tickers_list)} ticker saham dari CSV.")

# Looping untuk mengambil data dari yfinance berdasarkan ticker
for kode_saham in tickers_list:
    print(f"Mengambil data saham {kode_saham} dari yfinance...")

    try:
        saham = yf.Ticker(kode_saham)
        data_saham = saham.history(period="1mo")  # Ambil data 1 bulan terakhir

        if data_saham.empty:
            print(f"Data kosong untuk {kode_saham}")
            continue

        # Konversi ke format dictionary (JSON)
        data_saham.reset_index(inplace=True)
        json_saham = data_saham.to_dict(orient="records")

        # Tambahkan kode saham sebelum menyimpannya ke MongoDB
        json_saham = [{"kode_saham": kode_saham, **record} for record in json_saham]

        # Simpan ke MongoDB
        yfinance_collection.insert_many(json_saham)
        print(f"Data saham {kode_saham} berhasil disimpan ke MongoDB!")

    except Exception as e:
        print(f"ERROR: Gagal mengambil data {kode_saham}: {e}")

    # Tunggu sebentar agar tidak terkena rate limit dari Yahoo Finance
    time.sleep(2)

print("Semua data saham selesai diproses!")