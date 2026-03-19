import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

class FullyAutomatedScraper:
    def __init__(self):
        print("Membuka browser (Mode Stealth CDP Masking)...")
        self.options = uc.ChromeOptions()
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--lang=id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7')
        
        # Menambahkan User-Agent yang lebih spesifik dan terlihat natural
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = uc.Chrome(options=self.options, use_subprocess=True)
        self.driver.maximize_window()

        # =================================================================
        # TEKNIK CDP MASKING: Menghapus jejak Selenium dari dalam browser
        # =================================================================
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.chrome = {
                    runtime: {}
                };
                const originalQuery = window.navigator.permissions.query;
                return window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """
        })

    def bypass_cloudflare_otomatis(self):
        try:
            cf_iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe[src*='cloudflare']")
            print("Terdeteksi hadangan Cloudflare! Memulai Auto-Bypass...")
            time.sleep(random.uniform(4.5, 7.5)) 
            
            self.driver.switch_to.frame(cf_iframe)
            checkbox = self.driver.find_element(By.CSS_SELECTOR, "body")
            
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(checkbox, random.randint(10, 20), random.randint(10, 20)).perform()
            time.sleep(random.uniform(0.5, 1.2))
            actions.click().perform()
            print("Klik bypass dieksekusi!")
            
            self.driver.switch_to.default_content()
            time.sleep(random.uniform(5.0, 8.0)) 
        except NoSuchElementException:
            pass
        except Exception:
            self.driver.switch_to.default_content()

    def tutup_popup_jika_ada(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='close'], button.css-yi9ndv")
            btn.click()
            time.sleep(random.uniform(1.0, 2.0))
        except:
            pass

    def scrape_keyword_page_1_only(self, keyword):
        query = keyword.replace(" ", "+")
        url = f"https://id.indeed.com/jobs?q={query}&l=Indonesia"
        
        data_ekstrak = []
        print(f"\nMenjalankan ekstraksi untuk: {keyword.upper()}")
        
        time.sleep(random.uniform(2.0, 4.0))
        self.driver.get(url)
        time.sleep(5)
        self.bypass_cloudflare_otomatis()
        
        try:
            self.tutup_popup_jika_ada()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
            )
            
            total_cards = len(self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon"))
            print(f"Mengekstrak {total_cards} elemen dari halaman...")
            
            for i in range(total_cards):
                cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
                if i >= len(cards): break
                card = cards[i]
                
                judul = deskripsi = perusahaan = lokasi = gaji = kualifikasi = link_stabil = jenis_pekerjaan = ""
                
                # --- AMBIL DATA PANEL KIRI ---
                try: 
                    title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                    judul = title_elem.text.strip()
                    job_key = title_elem.get_attribute("data-jk") 
                    if job_key: link_stabil = f"https://id.indeed.com/viewjob?jk={job_key}"
                except: 
                    job_key = None

                if not judul or judul == "": judul = "-"
                try: perusahaan = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
                except: perusahaan = "-"
                try: lokasi = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
                except: lokasi = "-"

                # --- BUKA DAN EKSTRAK PANEL KANAN (DETAIL) ---
                try:
                    teks_lama = ""
                    try: teks_lama = self.driver.find_element(By.ID, "jobDescriptionText").text
                    except: pass

                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_elem)
                    time.sleep(random.uniform(1.0, 2.5)) 
                    
                    try:
                        self.driver.execute_script("arguments[0].click();", title_elem)
                    except ElementClickInterceptedException:
                        self.tutup_popup_jika_ada()
                        self.driver.execute_script("arguments[0].click();", title_elem)
                    
                    if job_key:
                        try: WebDriverWait(self.driver, 10).until(EC.url_contains(job_key))
                        except TimeoutException: pass 
                    
                    sukses_load = False
                    try:
                        WebDriverWait(self.driver, 15).until(
                            lambda d: d.find_element(By.ID, "jobDescriptionText").text != teks_lama and len(d.find_element(By.ID, "jobDescriptionText").text.strip()) > 10
                        )
                        sukses_load = True
                    except TimeoutException:
                        print(f"[WARNING] {judul} (Detail gagal dimuat / Race Condition - TETAP DISIMPAN)")
                    
                    time.sleep(random.uniform(1.0, 2.0)) 
                    
                    try:
                        info_header = self.driver.find_element(By.ID, "salaryInfoAndJobType").text.split('\n')
                        for item in info_header:
                            item_lower = item.lower()
                            if "rp" in item_lower or "sebulan" in item_lower or "setahun" in item_lower: gaji = item
                            elif "waktu" in item_lower or "part-time" in item_lower or "full-time" in item_lower or "kontrak" in item_lower or "magang" in item_lower or "tetap" in item_lower or "freelance" in item_lower: jenis_pekerjaan = item
                    except: pass

                    if not jenis_pekerjaan:
                        try:
                            labels = self.driver.find_elements(By.XPATH, "//*[normalize-space(text())='Jenis lowongan' or normalize-space(text())='Job type']")
                            for label in labels:
                                parent_text = label.find_element(By.XPATH, "..").text.split('\n')
                                for j, baris in enumerate(parent_text):
                                    if baris.strip().lower() in ["jenis lowongan", "job type"]:
                                        if j + 1 < len(parent_text):
                                            jenis_pekerjaan = parent_text[j+1].strip()
                                            break
                                if jenis_pekerjaan: break
                        except: pass

                    deskripsi_container = self.driver.find_element(By.ID, "jobDescriptionText")
                    baris_teks = deskripsi_container.text.split('\n')
                    
                    deskripsi_lines = []
                    kualifikasi_lines = []
                    state = "deskripsi" 
                    
                    keyword_kualifikasi = ["qualification", "kualifikasi", "requirement", "persyaratan", "syarat", "ideally have", "what you need", "keterampilan", "looking for"]
                    keyword_jobdesc = ["job description", "deskripsi pekerjaan", "tanggung jawab", "responsibilit", "what you will do", "day-to-day", "the role", "tugas", "tentang pekerjaan", "about the job"]
                    keyword_company = ["about us", "tentang kami", "about team", "company description", "tentang perusahaan", "who we are", "company overview", "tentang"]
                    
                    for line in baris_teks:
                        line_clean = line.strip()
                        line_lower = line_clean.lower()
                        if not line_clean: continue
                        
                        if len(line_lower) < 45:
                            is_header = False
                            if line_lower.startswith("about ") or any(kw in line_lower for kw in keyword_company):
                                state = "company"
                                is_header = True
                            elif any(kw in line_lower for kw in keyword_kualifikasi):
                                state = "kualifikasi"
                                is_header = True
                            elif any(kw in line_lower for kw in keyword_jobdesc):
                                state = "deskripsi"
                                is_header = True
                            if is_header: continue 
                        
                        if state == "kualifikasi":
                            clean_bullet = line_clean.lstrip('•-*▪❖✓').strip()
                            if clean_bullet: kualifikasi_lines.append(clean_bullet)
                        elif state == "deskripsi":
                            deskripsi_lines.append(line_clean)
                        elif state == "company":
                            pass 
                            
                    deskripsi = "\n".join(deskripsi_lines).strip()
                    kualifikasi = " | ".join(kualifikasi_lines).strip()
                    if not deskripsi: deskripsi = "-"
                    if not kualifikasi: kualifikasi = "-"
                except Exception:
                    deskripsi = "-"
                    kualifikasi = "-"

                if judul == "-" or kualifikasi == "-" or deskripsi == "-":
                    print(f"  ❌ [DIBUANG] {judul} (Data tidak lengkap)")
                    continue

                job_dict = {
                    "Judul_Pekerjaan": judul,
                    "Jenis_Pekerjaan": jenis_pekerjaan if jenis_pekerjaan else "-",
                    "Nama_Perusahaan": perusahaan,
                    "Lokasi": lokasi,
                    "Rentang_Gaji": gaji if gaji else "-",
                    "Kualifikasi_Persyaratan": kualifikasi,
                    "Deskripsi_Pekerjaan": deskripsi,
                    "Link_Lowongan": link_stabil if link_stabil else "-"
                }

                data_ekstrak.append(job_dict)
                print(f"[DISIMPAN SEMENTARA] {job_dict['Judul_Pekerjaan']}")

        except TimeoutException:
            print("Gagal memuat lowongan di panel kiri. Koneksi lambat atau diblokir Cloudflare.")
            
        return data_ekstrak

    def close(self):
        try:
            self.driver.quit()
            print("Browser berhasil ditutup dengan aman.")
        except Exception:
            pass