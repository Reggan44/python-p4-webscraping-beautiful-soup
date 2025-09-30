# Web Scraping with Beautiful Soup - Learning Project

This repository demonstrates web scraping concepts using Python's Beautiful Soup library and the requests module. It includes comprehensive examples from basic concepts to advanced practical applications.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ 
- pip or pipenv

### Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pipenv install && pipenv shell
   ```
   Or with pip:
   ```bash
   pip install requests beautifulsoup4
   ```

## 📁 Project Structure

```
lib/
├── scraper.py              # Main scraping demonstrations
├── advanced_examples.py    # Advanced Beautiful Soup techniques  
└── practical_example.py    # Real-world scraping project
```

## 🎯 Learning Objectives

After working through these examples, you'll understand:

- **Web scraping fundamentals** - What it is and why it's useful
- **HTTP requests** - Using the `requests` library to fetch web pages
- **HTML parsing** - Using Beautiful Soup to parse and navigate HTML
- **CSS selectors** - Finding elements using classes, IDs, and attributes
- **Data extraction** - Getting text content and attributes from elements
- **Error handling** - Dealing with network issues and missing elements
- **Best practices** - Respectful scraping, data validation, and output formats

## 🔧 Examples Overview

### 1. Basic Scraping (`scraper.py`)

Demonstrates fundamental concepts:
- Making HTTP requests with headers
- Parsing HTML with Beautiful Soup
- Using CSS selectors to find elements
- Extracting text and attributes
- Basic error handling

**Run it:**
```python
python lib/scraper.py
```

### 2. Advanced Techniques (`advanced_examples.py`)

Covers sophisticated Beautiful Soup usage:
- Complex CSS selector patterns
- Element methods and properties (.attrs, .contents, .children)
- Tree navigation (parent, siblings)
- Iterating over element collections
- Robust error handling strategies

**Run it:**
```python
python lib/advanced_examples.py
```

### 3. Practical Application (`practical_example.py`)

A complete scraping project that:
- Scrapes multiple pages with pagination
- Implements respectful delays between requests
- Analyzes and summarizes collected data
- Saves data in multiple formats (JSON, CSV, TXT)
- Uses sessions for efficient scraping
- Handles relative/absolute URLs

**Run it:**
```python
python lib/practical_example.py
```

## 🔍 Key Beautiful Soup Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `BeautifulSoup(html, 'html.parser')` | Parse HTML string | `doc = BeautifulSoup(html.text, 'html.parser')` |
| `.select(selector)` | Find elements by CSS selector | `doc.select('.heading-60-black.color-black.mb-20')` |
| `.select_one(selector)` | Find first matching element | `title = doc.select_one('h1')` |
| `.find(tag)` | Find first element by tag | `first_p = doc.find('p')` |
| `.find_all(tag)` | Find all elements by tag | `all_links = doc.find_all('a')` |
| `.get_text()` | Extract text content | `text = element.get_text(strip=True)` |
| `.get(attribute)` | Get attribute value | `href = link.get('href')` |

## 🎨 CSS Selector Examples

```python
# By ID
doc.select('#main-content')

# By single class
doc.select('.title')

# By multiple classes (all must match)
doc.select('.heading-60-black.color-black.mb-20')

# By tag name
doc.select('div')

# By attribute
doc.select('a[href]')

# Descendant selector
doc.select('.section h2')

# Direct child selector
doc.select('.navigation > li')
```

## 🛡️ Best Practices Demonstrated

1. **Respectful Scraping**
   - Add delays between requests (`time.sleep()`)
   - Use proper User-Agent headers
   - Handle rate limiting gracefully

2. **Error Handling**
   - Check if elements exist before accessing properties
   - Handle network timeouts and connection errors
   - Validate data before processing

3. **Code Organization**
   - Separate concerns (scraping, analysis, saving)
   - Use functions for reusable logic
   - Add comprehensive documentation

4. **Data Management**
   - Clean and validate scraped data
   - Save in multiple formats for different uses
   - Include metadata (timestamps, source URLs)

## 📊 Sample Output

The practical example scrapes quotes and generates:

- **quotes.json** - Structured data for programmatic use
- **quotes.csv** - Tabular format for spreadsheet applications  
- **quotes_summary.txt** - Human-readable summary report

## ⚠️ Important Notes

- **Legal Considerations**: Always check a website's `robots.txt` and terms of service
- **Rate Limiting**: Be respectful with request frequency
- **Dynamic Content**: These examples work with static HTML; JavaScript-rendered content requires additional tools
- **Maintenance**: Scrapers may break when websites update their structure

## 🔗 Resources

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.asp)
- [quotes.toscrape.com](http://quotes.toscrape.com/) - Practice scraping site

## 🧪 Running Tests

```bash
pytest
```

## 📝 License

This project is for educational purposes. Please respect website terms of service when scraping.