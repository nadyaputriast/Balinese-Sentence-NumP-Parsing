import asyncio
import json
from playwright.async_api import async_playwright
import time

class GlosbeScraper:
    def __init__(self, max_words=5, delay_seconds=5):
        self.max_words = max_words
        self.delay_seconds = delay_seconds
        self.words_data = []
        
    async def scrape_word_list(self, page_num=1):
        """Scrape the recent translations list to get word IDs"""
        async with async_playwright() as p:
            # Launch browser with proper user agent
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="BalineseResearchBot/1.0 (Linguistic Research; Contact: nadyaputriast@gmail.com)"
            )
            page = await context.new_page()
            
            print(f"🔍 Fetching word list from page {page_num}...")
            url = f"https://app.glosbe.com/recent?l1=id&l2=ban&user=&page={page_num}"
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for content to load
                await page.wait_for_selector('a[href*="/translation?id="]', timeout=10000)
                
                # Extract translation links
                links = await page.query_selector_all('a[href*="/translation?id="]')
                
                word_ids = []
                for link in links[:self.max_words]:
                    href = await link.get_attribute('href')
                    if href and 'id=' in href:
                        # Extract ID from URL
                        word_id = href.split('id=')[1].split('#')[0].split('&')[0]
                        word_ids.append(word_id)
                
                print(f"✅ Found {len(word_ids)} word IDs to process")
                
                await browser.close()
                return word_ids
                
            except Exception as e:
                print(f"❌ Error fetching word list: {e}")
                await browser.close()
                return []

    async def scrape_word_details(self, word_id):
        """Scrape details for a specific word"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="BalineseResearchBot/1.0 (Linguistic Research; Contact: nadyaputriast@gmail.com)"
            )
            page = await context.new_page()
            
            url = f"https://app.glosbe.com/translation?id={word_id}"
            print(f"📖 Scraping word ID: {word_id}")
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for content to load
                await asyncio.sleep(2)
                
                # Setup dictionary struktur awal
                word_data = {
                    'id': word_id,
                    'indonesian': None,
                    'balinese': None,
                    'url': url,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Mencari elemen td yang memiliki atribut lang Bali dan Indonesia
                balinese_elem = await page.query_selector('td[lang="ban"]')
                indonesian_elem = await page.query_selector('td[lang="id"]')
                
                if balinese_elem and indonesian_elem:
                    balinese_text = await balinese_elem.inner_text()
                    indonesian_text = await indonesian_elem.inner_text()
                    
                    # Simpan dan bersihkan teks
                    word_data['balinese'] = balinese_text.strip()
                    word_data['indonesian'] = indonesian_text.strip()
                
                print(f"  ✓ {word_data['indonesian']} → {word_data['balinese']}")
                
                await browser.close()
                return word_data
                
            except Exception as e:
                print(f"  ❌ Error scraping word {word_id}: {e}")
                await browser.close()
                return None

    async def run(self):
        """Main scraping workflow"""
        print("="*60)
        print("🚀 GLOSBE SCRAPER - PROOF OF CONCEPT")
        print(f"📊 Target: {self.max_words} words")
        print(f"⏱️  Delay: {self.delay_seconds} seconds between requests")
        print("="*60)
        print()
        
        # Step 1: Get word IDs from listing page
        word_ids = await self.scrape_word_list(page_num=1)
        
        if not word_ids:
            print("❌ Failed to fetch word IDs. Exiting.")
            return
            
        print(f"\n📝 Starting detailed scraping of {min(len(word_ids), self.max_words)} words...")
        print()
        
        # Step 2: Scrape details for each word
        for i, word_id in enumerate(word_ids[:self.max_words], 1):
            print(f"\n[{i}/{min(len(word_ids), self.max_words)}]", end=" ")
            
            word_data = await self.scrape_word_details(word_id)
            
            if word_data:
                self.words_data.append(word_data)
            
            # Respectful delay between requests
            if i < min(len(word_ids), self.max_words):
                print(f"  ⏸️  Waiting {self.delay_seconds} seconds...")
                await asyncio.sleep(self.delay_seconds)
                
        # Step 3: Save results
        self.save_results()

    def save_results(self):
        """Save scraped data to JSON file"""
        # File disave di folder yang sama dengan script
        output_file = 'glosbe_balinese_words_poc.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.words_data, f, ensure_ascii=False, indent=2)
            
        print("\n" + "="*60)
        print("✅ SCRAPING COMPLETE!")
        print(f"📁 Saved {len(self.words_data)} words to: {output_file}")
        print("="*60)
        
        # Print summary
        print("\n📊 SUMMARY:")
        print(f"  Total words scraped: {len(self.words_data)}")
        successful = sum(1 for w in self.words_data if w.get('indonesian') and w.get('balinese'))
        print(f"  Successful extractions: {successful}")
        print(f"  Failed extractions: {len(self.words_data) - successful}")
        
        if self.words_data:
            print("\n🔍 SAMPLE DATA:")
            for word in self.words_data[:3]:
                print(f"  • {word.get('indonesian', 'N/A')} → {word.get('balinese', 'N/A')}")


async def main():
    """Run the scraper"""
    scraper = GlosbeScraper(
        max_words=5,
        delay_seconds=7  
    )
    
    await scraper.run()


if __name__ == "__main__":
    print("\n⚠️  IMPORTANT NOTES:")
    print("  - This is a proof of concept for linguistic research")
    print("  - Using respectful scraping practices")
    print("\n")
    
    asyncio.run(main())