import requests
from bs4 import BeautifulSoup

def scrape_pib_text(url):
    """Scrapes the main press release text from a PIB URL."""
    print(f"Attempting to scrape URL: {url}\n")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Will raise an error for 4xx/5xx responses
        print(f"Response: {response.status_code} OK")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # We now look for multiple selectors in order of priority
        selectors = [
            'span.blogdescription',  # --- CORRECTED SELECTOR for blogs.pib.gov.in ---
            'div.content-area',      # Selector 1 (for URLs like 2188503)
            'div.Release-content',   # Selector 2 (Old layout)
            'div#pressrelease',    # Selector 3 (Older layout)
            'div.inn-left-cont'    # Selector 4 (Another common layout)
        ]
        
        content_div = None
        for selector in selectors:
            content_div = soup.select_one(selector)
            if content_div:
                print(f"Found content with selector: '{selector}'")
                break # Found one, stop looking
        
        if content_div:
            # Get text from all <p> tags within the found div
            paragraphs = content_div.find_all('p')
            
            main_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

            # Fallback if no <p> tags were found, just get all text
            if not main_text.strip():
                 print("No <p> tags found, falling back to all text.")
                 main_text = content_div.get_text(strip=True)
                 
            return main_text.strip()
        else:
            print("ERROR: No content selectors matched.")
            return None # Return None to trigger the error message
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

if __name__ == "__main__":
    # --- THIS IS THE URL YOU PROVIDED ---
    test_url = "https://blogs.pib.gov.in/blogsdescr.aspx?feaaid=394"
    
    print("--- STARTING SCRAPER TEST ---")
    scraped_data = scrape_pib_text(test_url)
    
    if scraped_data:
        print("\n--- SCRAPE SUCCESSFUL ---")
        print("First 200 characters:")
        print(scraped_data[:200] + "...")
    else:
        print("\n--- SCRAPE FAILED ---")
        print("The function returned None.")
    print("--- END OF TEST ---")
