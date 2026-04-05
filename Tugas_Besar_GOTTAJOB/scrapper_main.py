import json
import time
import random
from scraper import FullyAutomatedScraper # Memanggil mesin bot dari file scraper.py

if __name__ == "__main__":
    KATEGORI_PEKERJAAN = {
        "web_developer.json": [
            "web developer jakarta", 
            "frontend developer indonesia", 
            "backend developer indonesia"
        ],
        "game_developer.json": [
            "game developer indonesia", 
            "unity developer indonesia",
            "junior game developer indonesia"
        ],
        "mobile_developer.json": [
            "mobile developer jakarta", 
            "android developer indonesia",
            "ios developer indonesia"
        ],
        "cyber_security.json": [
            "cyber security indonesia", 
            "security engineer jakarta",
            "junior cyber security indonesia"
        ]
    }
    
    # GLOBAL TRACKER: Untuk mencegah redundansi/duplikasi data lintas-file
    global_seen_links = set()
    total_duplikat_lintas_file = 0
    
    for nama_file, list_keywords in KATEGORI_PEKERJAAN.items():
        print(f"\n==================================================")
        print(f"MEMULAI PROSES PENGUMPULAN UNTUK FILE: {nama_file}")
        print(f"==================================================")
        
        # Panggil mesin bot yang ada di scraper.py
        mesin_scraper = FullyAutomatedScraper()
        data_mentah_kategori = []
        
        try:
            for kw in list_keywords:
                hasil_scraping = mesin_scraper.scrape_keyword_page_1_only(kw)
                data_mentah_kategori.extend(hasil_scraping)
                
                # JEDA ANTAR KATA KUNCI DIPERLAMBAT AGAR LEBIH NATURAL
                waktu_jeda = random.uniform(15.0, 25.0)
                print(f"Jeda panjang {waktu_jeda:.1f} detik sebelum variasi keyword berikutnya...")
                time.sleep(waktu_jeda)
                
            # PROSES PENYARINGAN & PENYIMPANAN DATA (DEDUPLIKASI)
            if data_mentah_kategori:
                data_bersih_unik = []
                duplikat_lokal = 0
                
                for job in data_mentah_kategori:
                    link = job["Link_Lowongan"]
                    
                    # Cek apakah Link URL ini sudah pernah ada di database kita
                    if link != "-" and link in global_seen_links:
                        duplikat_lokal += 1
                        total_duplikat_lintas_file += 1
                        continue # Skip data ini karena redundan
                        
                    # Jika datanya unik, catat linknya dan simpan datanya
                    if link != "-":
                        global_seen_links.add(link)
                    data_bersih_unik.append(job)
                
                # Simpan data yang sudah disaring ke JSON
                with open(nama_file, 'w', encoding='utf-8') as f:
                    json.dump(data_bersih_unik, f, ensure_ascii=False, indent=4)
                    
                print(f"\nBERHASIL! {len(data_bersih_unik)} data UNIK tersimpan ke '{nama_file}'.")
                if duplikat_lokal > 0:
                    print(f"Info: {duplikat_lokal} data dibuang karena duplikat/redundan.")
            else:
                print(f"\nTidak ada data yang berhasil dikumpulkan untuk '{nama_file}'")
                
        except Exception as e:
            print(f"\nError eksekusi: {e}")
        finally:
            time.sleep(2)
            mesin_scraper.close() 
            
        print("\nMemberikan jeda 8 detik sebelum mengganti Kategori Pekerjaan utama...")
        time.sleep(8)

    print("\n==================================================")
    print(f"SEMUA EKSEKUSI OTOMATIS SELESAI!")
    print(f"Total Data Unik Keseluruhan Database: {len(global_seen_links)}")
    print(f"Total Data Duplikat yang Berhasil Dihindari: {total_duplikat_lintas_file}")
    print("==================================================")