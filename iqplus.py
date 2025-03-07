from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymongo

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bigdata"]
berita_collection = db["IQplus"]  # Koleksi tempat menyimpan data berita

# Konfigurasi Microsoft Edge WebDriver
options = webdriver.EdgeOptions()
options.add_argument("--headless")  # Mode tanpa tampilan browser
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Buka WebDriver
driver = webdriver.Edge(options=options)
url = "http://www.iqplus.info/index.php"
driver.get(url)
time.sleep(5)  # Tunggu halaman termuat

# Ambil daftar berita terbaru
berita_elements = driver.find_elements(By.XPATH, "//ul[@class='news']/li/a")  # Ambil semua berita
tanggal_elements = driver.find_elements(By.XPATH, "//ul[@class='news']/li/b")  # Ambil semua tanggal

berita_links = []
for i in range(len(berita_elements)):
    try:
        berita_url = berita_elements[i].get_attribute("href")
        judul = berita_elements[i].text.strip()
        tanggal = tanggal_elements[i].text.strip() if i < len(tanggal_elements) else "Tidak Diketahui"

        berita_links.append({
            "judul": judul,
            "url": berita_url,
            "tanggal": tanggal
        })
    except Exception as e:
        print(f"ERROR mengambil berita ke-{i}: {e}")

print(f"Ditemukan {len(berita_links)} berita.")

# Looping untuk mengambil isi berita
for berita in berita_links[:10]:  # Ambil 10 berita pertama
    print(f"Mengambil berita dari: {berita['url']}")

    # Buka halaman berita
    driver.get(berita['url'])
    time.sleep(3)

    try:
        # **Mengambil isi berita dari <div id="zoomthis">**
        isi_berita = driver.find_element(By.XPATH, "//div[@id='zoomthis']").text.strip()

        # Simpan ke MongoDB
        berita_data = {
            "judul": berita["judul"],
            "tanggal": berita["tanggal"],
            "url": berita["url"],
            "isi": isi_berita
        }
        berita_collection.insert_one(berita_data)

        print(f"Berita '{berita['judul']}' berhasil disimpan ke MongoDB!")

    except Exception as e:
        print(f"ERROR: Gagal mengambil isi berita dari {berita['url']}: {e}")

    # Tunggu sebentar agar tidak terdeteksi sebagai bot
    time.sleep(2)

# Tutup browser setelah selesai
driver.quit()

print("Semua berita selesai diproses!")
