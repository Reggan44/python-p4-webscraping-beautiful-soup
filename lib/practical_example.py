"""
Practical Web Scraping Example
A real-world scenario demonstrating how to build a complete web scraper.
"""

from bs4 import BeautifulSoup
import requests
import csv
import json
from urllib.parse import urljoin, urlparse


def scrape_quotes_to_scrape():
    """
    Scrapes quotes from quotes.toscrape.com - a site designed for practicing scraping.
    This demonstrates a complete scraping workflow.
    """
    print("=== Scraping Quotes from quotes.toscrape.com ===")
    
    base_url = "http://quotes.toscrape.com"
    headers = {'user-agent': 'learning-scraper/1.0'}
    
    all_quotes = []
    page = 1
    
    while True:
        url = f"{base_url}/page/{page}/"
        print(f"Scraping page {page}...")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            doc = BeautifulSoup(response.text, 'html.parser')
            
            # Find all quote containers
            quotes = doc.select('.quote')
            
            if not quotes:
                print("No more quotes found. Scraping complete!")
                break
            
            for quote in quotes:
                # Extract quote text
                text_elem = quote.select_one('.text')
                text = text_elem.get_text(strip=True) if text_elem else "No text"
                
                # Extract author
                author_elem = quote.select_one('.author')
                author = author_elem.get_text(strip=True) if author_elem else "Unknown"
                
                # Extract tags
                tag_elements = quote.select('.tag')
                tags = [tag.get_text(strip=True) for tag in tag_elements]
                
                quote_data = {
                    'text': text,
                    'author': author,
                    'tags': tags,
                    'page': page
                }
                
                all_quotes.append(quote_data)
                print(f"  Found quote by {author}")
            
            # Check if there's a next page
            next_btn = doc.select_one('.next')
            if not next_btn:
                print("Reached the last page!")
                break
                
            page += 1
            
            # Be respectful - add a small delay
            import time
            time.sleep(0.5)
            
        except requests.RequestException as e:
            print(f"Error scraping page {page}: {e}")
            break
    
    print(f"\nScraping completed! Total quotes collected: {len(all_quotes)}")
    return all_quotes


def analyze_scraped_data(quotes):
    """
    Analyzes the scraped quotes data to show insights.
    """
    print("\n=== Data Analysis ===")
    
    if not quotes:
        print("No quotes to analyze!")
        return
    
    # Count quotes by author
    author_counts = {}
    for quote in quotes:
        author = quote['author']
        author_counts[author] = author_counts.get(author, 0) + 1
    
    print("Top authors by number of quotes:")
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    for author, count in sorted_authors[:5]:
        print(f"  {author}: {count} quotes")
    
    # Collect all tags
    all_tags = []
    for quote in quotes:
        all_tags.extend(quote['tags'])
    
    # Count tag frequency
    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    print(f"\nMost common tags:")
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    for tag, count in sorted_tags[:10]:
        print(f"  {tag}: {count} times")
    
    # Find longest and shortest quotes
    quote_lengths = [(len(quote['text']), quote['text'], quote['author']) for quote in quotes]
    quote_lengths.sort(key=lambda x: x[0])
    
    shortest = quote_lengths[0]
    longest = quote_lengths[-1]
    
    print(f"\nShortest quote ({shortest[0]} chars) by {shortest[2]}:")
    print(f"  \"{shortest[1]}\"\n")
    
    print(f"Longest quote ({longest[0]} chars) by {longest[2]}:")
    print(f"  \"{longest[1][:100]}...\"" if len(longest[1]) > 100 else f"  \"{longest[1]}\"")


def save_data_to_files(quotes):
    """
    Saves the scraped data in multiple formats.
    """
    print("\n=== Saving Data ===")
    
    if not quotes:
        print("No quotes to save!")
        return
    
    # Save as JSON
    json_filename = "quotes.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(quotes)} quotes to {json_filename}")
    
    # Save as CSV
    csv_filename = "quotes.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        if quotes:
            writer = csv.DictWriter(f, fieldnames=['text', 'author', 'tags', 'page'])
            writer.writeheader()
            
            for quote in quotes:
                # Convert tags list to string for CSV
                csv_quote = quote.copy()
                csv_quote['tags'] = ', '.join(quote['tags'])
                writer.writerow(csv_quote)
    
    print(f"Saved {len(quotes)} quotes to {csv_filename}")
    
    # Save a simple text summary
    txt_filename = "quotes_summary.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("QUOTES COLLECTION SUMMARY\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Total quotes: {len(quotes)}\n")
        
        authors = set(quote['author'] for quote in quotes)
        f.write(f"Unique authors: {len(authors)}\n\n")
        
        f.write("Sample quotes:\n")
        for i, quote in enumerate(quotes[:5], 1):
            f.write(f"{i}. \"{quote['text']}\" - {quote['author']}\n")
    
    print(f"Saved summary to {txt_filename}")


def scrape_with_session():
    """
    Demonstrates using a requests Session for more efficient scraping.
    """
    print("\n=== Using Session for Efficient Scraping ===")
    
    # Create a session to reuse connections
    session = requests.Session()
    session.headers.update({'user-agent': 'learning-scraper/1.0'})
    
    urls_to_test = [
        "http://quotes.toscrape.com/",
        "http://quotes.toscrape.com/page/2/",
        "http://quotes.toscrape.com/random",
    ]
    
    for url in urls_to_test:
        try:
            response = session.get(url)
            response.raise_for_status()
            
            doc = BeautifulSoup(response.text, 'html.parser')
            
            # Count quotes on this page
            quotes = doc.select('.quote')
            
            print(f"  {url}: {len(quotes)} quotes found")
            
        except requests.RequestException as e:
            print(f"  {url}: Error - {e}")
    
    # Always close the session when done
    session.close()


def demonstrate_link_extraction():
    """
    Shows how to extract and work with links from web pages.
    """
    print("\n=== Link Extraction Demo ===")
    
    headers = {'user-agent': 'learning-scraper/1.0'}
    
    try:
        response = requests.get("http://quotes.toscrape.com/", headers=headers)
        response.raise_for_status()
        
        doc = BeautifulSoup(response.text, 'html.parser')
        base_url = "http://quotes.toscrape.com"
        
        # Find all links
        links = doc.select('a[href]')
        
        print(f"Found {len(links)} links:")
        
        unique_links = set()
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Convert relative URLs to absolute URLs
            full_url = urljoin(base_url, href)
            
            if full_url not in unique_links:
                unique_links.add(full_url)
                print(f"  '{text}' -> {full_url}")
        
        print(f"\nTotal unique links: {len(unique_links)}")
        
    except requests.RequestException as e:
        print(f"Error extracting links: {e}")


def main():
    """
    Run the complete practical scraping example.
    """
    print("Practical Web Scraping Example")
    print("=" * 50)
    
    # Scrape the quotes
    quotes = scrape_quotes_to_scrape()
    
    # Analyze the data
    analyze_scraped_data(quotes)
    
    # Save the data
    save_data_to_files(quotes)
    
    # Demonstrate session usage
    scrape_with_session()
    
    # Show link extraction
    demonstrate_link_extraction()
    
    print("\n" + "=" * 50)
    print("Practical scraping example completed!")
    
    print("\nBest practices demonstrated:")
    print("- Respectful scraping with delays between requests")
    print("- Proper error handling for network issues")
    print("- Data validation and cleaning")
    print("- Multiple output formats (JSON, CSV, TXT)")
    print("- Using sessions for efficiency")
    print("- Handling relative vs absolute URLs")
    print("- Pagination handling")
    print("- Data analysis and insights")


if __name__ == "__main__":
    main()