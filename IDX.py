import os
import time
import json
import zipfile
import xmltodict
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient

def download_files(year, page):
    # Ambil semua tombol download instance.zip
    download_buttons = driver.find_elements(By.XPATH, "//a[contains(@href, 'instance.zip')]")
    print(f"Jumlah tombol download ditemukan: {len(download_buttons)}")

    if len(download_buttons) == 0:
        print("GAGAL: Tidak ada tombol download ditemukan!")
    else:
        for index, button in enumerate(download_buttons):
            print(f"Mengunduh file ke-{index+1} ({year} - {page})...")
            existing_files = set(os.listdir(download_folder))
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)

            # Cari file baru yang terunduh
            new_files = set(os.listdir(download_folder)) - existing_files
            if not new_files:
                print("ERROR: Download gagal atau tidak ditemukan!")
                continue

            zip_path = os.path.join(download_folder, list(new_files)[0])
            print(f"ZIP file tersimpan: {zip_path}")

            # Periksa apakah file benar-benar ZIP
            with open(zip_path, "rb") as f:
                file_header = f.read(4)
                if file_header != b"PK\x03\x04":
                    print(f"ERROR: {zip_path} bukan file ZIP yang valid!")
                    continue

            try:
                with zipfile.ZipFile(zip_path, "r") as zip_file:
                    print("ZIP file berhasil dibuka.")

                    # Pastikan ada file taxonomy.xsd
                    if "Taxonomy.xsd" not in zip_file.namelist():
                        print("ERROR: Tidak menemukan 'Taxonomy.xsd' dalam ZIP!")
                        continue

                    # Parsing taxonomy.xsd
                    with zip_file.open("Taxonomy.xsd") as xsd_file: 
                        parent_element = download_buttons[index].find_element(By.XPATH, "ancestor::div[2]")
                        span_element = parent_element.find_element(By.XPATH, ".//span[contains(@class, 'f-20 f-m-30')]")
                        span_text = span_element.text
                        xsd_content = xsd_file.read()
                        xsd_dict = xmltodict.parse(xsd_content)

                        json_file = os.path.join(download_folder, f"{year}_{span_text}.json")
                        with open(json_file, 'w', encoding='utf-8') as file:
                            json.dump(xsd_dict, file, indent=4, ensure_ascii=False)
                        
                        print(f"Conversion successful! JSON saved as {json_file}")

                        # Add attributes to json_data
                        with open(json_file, 'r', encoding='utf-8') as file:
                            json_data = json.load(file)
                        json_data = {
                            'emitten': span_text,
                            'year': year,
                            'schema': json_data
                        }
                        
                        save_to_mongodb(json_data)

            except zipfile.BadZipFile:
                print("ERROR: File ZIP tidak valid!")
                continue

            os.remove(zip_path)
            print(f"ZIP file {zip_path} has been deleted.")

# Simpan ke MongoDB
def save_to_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bigdata"]
    collection = db["IDX"]
    
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    
    print("Data berhasil disimpan ke MongoDB.")

# Buat folder untuk menyimpan file ZIP
download_folder = os.path.abspath("downloads")
os.makedirs(download_folder, exist_ok=True)

# Konfigurasi Chrome WebDriver untuk otomatis download ZIP
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_folder,  # Simpan otomatis ke folder ini
    "download.prompt_for_download": False,  # Jangan tampilkan pop-up download
    "safebrowsing.enabled": True, # Aktifkan Safe Browsing
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

# Buka halaman IDX
print("Membuka halaman IDX...")
driver.get("https://www.idx.co.id/id/perusahaan-tercatat/laporan-keuangan-dan-tahunan")
time.sleep(3)

# Pilih Tahun
for _ in [2024, 2023, 2022, 2021]:
    if driver.find_element(By.XPATH, "//button[contains(text(), 'Terapkan')]") is None:
        driver.find_element(By.XPATH, "//button[contains(@class, 'btn-filter-input')]").click()
    tahun = driver.find_element(By.XPATH, f"//input[@value='{_}']")
    driver.execute_script("arguments[0].click();", tahun)
    print(f"Tahun {_} dipilih.")

    tahunan = driver.find_element(By.XPATH, "//input[@value='audit']")
    driver.execute_script("arguments[0].click();", tahunan)
    print("Tahunan dipilih.")

    apply = driver.find_element(By.XPATH, "//button[contains(text(), 'Terapkan')]")
    driver.execute_script("arguments[0].click();", apply)
    time.sleep(5)
    print("Tombol Terapkan diklik.")

    page = 1
    while True:
        download_files(_, page)
        next_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
        if next_button.get_attribute("disabled") is not None:
            print("Tidak ada halaman berikutnya. Proses selesai.")
            break
        else:
            print("Menuju ke halaman berikutnya...")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
            page += 1
    
# Cek jumlah dokumen di MongoDB
print("Semua data selesai diproses!")

driver.quit()