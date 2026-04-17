import asyncio
import json
import os
from playwright.async_api import async_playwright

class GlosbeKnowledgeBaseBuilder:
    def __init__(self, target_pos_dict, max_concurrent=5):
        self.target_dict = target_pos_dict 
        # max_concurrent = Jumlah tab yang dibuka bersamaan (Direkomendasikan: 3 sampai 8)
        self.max_concurrent = max_concurrent 
        self.output_file = 'balinese_lexicon.json'
        
        # Lock untuk mencegah tab bertabrakan saat menulis ke dictionary / file
        self.file_lock = asyncio.Lock()
        
        # Variabel untuk menghitung Log Progress
        self.total_words = sum(len(words) for words in self.target_dict.values())
        self.processed_words = 0
        self.success_words = 0
        
        # Fitur Resume: Load file jika sudah ada
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {pos: {} for pos in self.target_dict.keys()}
        
    async def scrape_word(self, context, semaphore, word, pos_category):
        """Mencari satu kata. Dijalankan bersamaan oleh banyak tab."""
        
        # Jika kata sudah ada di database, skip
        if word in self.knowledge_base[pos_category].values():
            async with self.file_lock:
                self.processed_words += 1
            return

        # Menunggu giliran tab kosong (Semaphore)
        async with semaphore:
            page = await context.new_page() # Buka Tab Baru
            url = f"https://glosbe.com/id/ban/{word}"
            found_translations = []
            
            try:
                # domcontentloaded lebih cepat dari networkidle
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(1) # Jeda render elemen
                
                translations = set()
                elements = await page.query_selector_all('.translation__item')
                if not elements:
                    elements = await page.query_selector_all('.dense-sense-list strong')
                
                for el in elements:
                    text = await el.inner_text()
                    if text:
                        clean_text = text.split('\n')[0].strip().lower()
                        if clean_text: translations.add(clean_text)
                
                # Update Data & Counter (Wajib pakai Lock agar thread-safe)
                async with self.file_lock:
                    for trans in translations:
                        if " " not in trans: # Buang frasa (spasi)
                            if trans not in self.knowledge_base[pos_category]:
                                self.knowledge_base[pos_category][trans] = word
                                found_translations.append(trans)
                    
                    self.processed_words += 1
                    if found_translations:
                        self.success_words += 1
                        
                # --- PRINT LOGGING YANG RAPI ---
                pct = (self.processed_words / self.total_words) * 100
                if found_translations:
                    print(f"[{self.processed_words}/{self.total_words}] ({pct:.1f}%) ✅ [{pos_category}] '{word}' -> {found_translations}")
                else:
                    print(f"[{self.processed_words}/{self.total_words}] ({pct:.1f}%) ⚠️ [{pos_category}] '{word}' -> Tidak ada / Berupa Frasa")
                
            except Exception as e:
                async with self.file_lock:
                    self.processed_words += 1
                error_msg = str(e).split('\n')[0][:40] # Ambil error sepotong aja biar rapi
                print(f"[{self.processed_words}/{self.total_words}] ❌ Error '{word}': {error_msg}...")
            finally:
                await page.close() # Wajib tutup tab setelah selesai
                
                # Auto-save tiap 20 kata selesai
                if self.processed_words % 20 == 0:
                    async with self.file_lock:
                        with open(self.output_file, 'w', encoding='utf-8') as f:
                            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=4)

    async def run(self):
        print("="*65)
        print(f"🚀 MEMULAI ASYNC CONCURRENT SCRAPING")
        print(f"⚙️  Membuka {self.max_concurrent} Tab Bersamaan")
        print(f"📊 Total Target: {self.total_words} kata")
        print("="*65)
        
        # 1. Buka Browser SEKALI SAJA di awal
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="BalineseParserBot/3.0")
            
            # 2. Siapkan Pengatur Antrean (Semaphore) dan Daftar Tugas (Tasks)
            semaphore = asyncio.Semaphore(self.max_concurrent)
            tasks = []
            
            for pos_category, words in self.target_dict.items():
                for word in words:
                    # Buat task untuk setiap kata, tapi jangan dijalankan dulu
                    task = asyncio.create_task(self.scrape_word(context, semaphore, word, pos_category))
                    tasks.append(task)
            
            # 3. JALANKAN SEMUA TUGAS SECARA CONCURRENT!
            await asyncio.gather(*tasks)
            
            await browser.close()
            
        # Final Save
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=4)
            
        print("\n" + "="*65)
        print(f"✅ SCRAPING SELESAI!")
        print(f"📈 Berhasil menemukan terjemahan untuk {self.success_words} kata.")
        print(f"📁 Data tersimpan aman di '{self.output_file}'")
        print("="*65)

async def main():
    try:
        with open('target_indo.json', 'r', encoding='utf-8') as f:
            kata_target = json.load(f)
    except FileNotFoundError:
        print("❌ File 'target_indo.json' tidak ditemukan! Jalankan 1_generate_indo.py dulu.")
        return

    # Set max_concurrent (berapa tab barengan). 
    # Saran: 5 itu pas. Kalau inet/laptop kuat bisa 8 atau 10. Jangan lebih dari 15 biar ga di ban.
    scraper = GlosbeKnowledgeBaseBuilder(target_pos_dict=kata_target, max_concurrent=5)
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())