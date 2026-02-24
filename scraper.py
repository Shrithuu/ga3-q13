from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    total_sum = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for seed in range(18, 28):  # Seeds 18 through 27
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Scraping seed {seed}...")
            
            page.goto(url)
            # Wait for the table to appear on the page
            page.wait_for_selector("table", timeout=10000)
            
            # Extract HTML and parse tables with Pandas
            html = page.content()
            tables = pd.read_html(html)
            
            if tables:
                df = tables[0]
                # Convert all data to numeric (forces text/errors to NaN), then sum
                numeric_df = df.apply(pd.to_numeric, errors='coerce')
                seed_sum = numeric_df.sum().sum()
                total_sum += seed_sum
                
        browser.close()
        
    print("-------------------------")
    print(f"GRAND TOTAL: {total_sum}")
    print("-------------------------")

if __name__ == "__main__":
    main()
