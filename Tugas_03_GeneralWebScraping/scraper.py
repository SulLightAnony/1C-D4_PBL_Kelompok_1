import time
import dateparser
import re
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ScraperThread(QThread):
    progress_update = pyqtSignal(int)
    data_received = pyqtSignal(dict)
    finished_scraping = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, base_url, limit, start_date, end_date):
        super().__init__()
        self.base_url = base_url
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.page_load_strategy = 'eager'
        
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.set_page_load_timeout(30)
            
            try:
                driver.get(self.base_url)
            except:
                driver.execute_script("window.stop();")
            
            time.sleep(4)
            
            js_links = """
            var links = document.querySelectorAll('a[href]');
            var result = [];
            var base = window.location.hostname.replace('www.', '');
            for(var i=0; i<links.length; i++) {
                var href = links[i].href;
                try {
                    var u = new URL(href);
                    if(u.hostname.includes(base)) {
                        var path = u.pathname.toLowerCase();
                        if(path.length > 25 && !path.includes('/tag/') && !path.includes('/category/') && !path.includes('/foto') && !path.includes('/video') && !path.includes('/indeks')) {
                            if(result.indexOf(href) === -1) {
                                result.push(href);
                            }
                        }
                    }
                } catch(e) {}
            }
            return result;
            """
            article_links = driver.execute_script(js_links)
            
            if not article_links:
                self.error_occurred.emit("Sistem tidak menemukan tautan artikel yang valid pada halaman utama situs ini.")
                driver.quit()
                return
            
            scraped_count = 0
            
            for link in article_links:
                if not self.is_running: break
                if scraped_count >= self.limit: break
                
                try:
                    driver.get(link)
                except:
                    driver.execute_script("window.stop();")
                
                time.sleep(2)
                
                js_extract = """
                var t = '';
                var d = '';
                var c = '';
                
                var scripts = document.querySelectorAll('script[type="application/ld+json"]');
                for (var i = 0; i < scripts.length; i++) {
                    try {
                        var data = JSON.parse(scripts[i].innerText);
                        var findDate = function(obj) {
                            if (obj.datePublished || obj.dateCreated || obj.uploadDate) {
                                return obj.datePublished || obj.dateCreated || obj.uploadDate;
                            }
                            return null;
                        };
                        
                        var extractedDate = null;
                        if (Array.isArray(data)) {
                            for (var j = 0; j < data.length; j++) {
                                extractedDate = findDate(data[j]);
                                if (extractedDate) break;
                            }
                        } else {
                            extractedDate = findDate(data);
                            if (!extractedDate && data['@graph']) {
                                for (var k = 0; k < data['@graph'].length; k++) {
                                    extractedDate = findDate(data['@graph'][k]);
                                    if (extractedDate) break;
                                }
                            }
                        }
                        if (extractedDate) { d = extractedDate; break; }
                    } catch(e) {}
                }
                
                if (!d) {
                    var selectors = [
                        'meta[property="article:published_time"]',
                        'meta[name="publishdate"]',
                        'meta[name="pubdate"]',
                        'meta[itemprop="datePublished"]',
                        'meta[property="og:updated_time"]',
                        'time[datetime]',
                        '.detail__date',
                        '.read__time',
                        '.date',
                        '.timestamp'
                    ];
                    for (var s of selectors) {
                        var el = document.querySelector(s);
                        if (el) {
                            d = el.content || el.getAttribute('datetime') || el.innerText;
                            if (d) break;
                        }
                    }
                }

                var h1 = document.querySelector('h1');
                if(h1) t = h1.innerText;
                
                var ps = document.querySelectorAll('p');
                var arr = [];
                for(var n=0; n<ps.length; n++) {
                    var txt = ps[n].innerText.strip ? ps[n].innerText.strip() : ps[n].innerText.trim();
                    if(txt.length > 50 && !txt.toLowerCase().includes('baca juga') && !txt.toLowerCase().includes('ads')) {
                        arr.push(txt);
                    }
                }
                c = arr.join('\\n\\n');
                
                return {title: t, content: c, date: d};
                """
                
                try:
                    extracted = driver.execute_script(js_extract)
                    title = extracted.get('title', '').strip()
                    content = extracted.get('content', '').strip()
                    date_raw = extracted.get('date', '').strip()
                    
                    clean_date = re.sub(r'(WIB|WITA|WIT|GMT|UTC|[a-zA-Z]{3}, \d{2} [a-zA-Z]+ \d{4} |\|)', '', date_raw).strip()
                    if not clean_date:
                        clean_date = date_raw
                        
                    parsed_date = dateparser.parse(clean_date, settings={'RELATIVE_BASE': datetime.now()})
                    
                    is_valid = True
                    if parsed_date:
                        parsed_date = parsed_date.replace(tzinfo=None)
                        if not (self.start_date <= parsed_date <= self.end_date):
                            is_valid = False
                    
                    if is_valid and title and content:
                        self.data_received.emit({
                            "title": title,
                            "date": parsed_date.strftime("%Y-%m-%d") if parsed_date else "Tidak Diketahui",
                            "content": content,
                            "url": link
                        })
                        scraped_count += 1
                        self.progress_update.emit(int((scraped_count / self.limit) * 100))
                except:
                    pass
                
            self.progress_update.emit(100)
            driver.quit()
            self.finished_scraping.emit(f"Selesai. {scraped_count} berita berhasil diambil.")
        except Exception as e:
            self.error_occurred.emit(str(e))