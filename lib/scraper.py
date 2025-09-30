from bs4 import BeautifulSoup
import requests


def scrape_flatiron_homepage():
    """
    Demonstrates basic web scraping using Beautiful Soup and requests.
    Scrapes the Flatiron School homepage for key information.
    """
    print("=== Scraping Flatiron School Homepage ===")
    
    # Set up headers to avoid bot detection
    headers = {'user-agent': 'my-app/0.0.1'}
    
    try:
        # Make HTTP request to get the HTML content
        html = requests.get("https://flatironschool.com/", headers=headers)
        html.raise_for_status()  # Raise exception for bad status codes
        
        # Create Beautiful Soup object to parse HTML
        doc = BeautifulSoup(html.text, 'html.parser')
        
        print(f"Successfully retrieved HTML content ({len(html.text)} characters)")
        
        # Example 1: Extract specific text using CSS selector
        # Look for headings with specific classes
        headings = doc.select('h1, h2, h3')  # Get all h1, h2, h3 elements
        
        if headings:
            print(f"\nFound {len(headings)} headings:")
            for i, heading in enumerate(headings[:5]):  # Show first 5
                text = heading.get_text(strip=True)
                if text:  # Only show non-empty text
                    print(f"{i+1}. {heading.name}: {text}")
        
        # Example 2: Extract navigation links
        nav_links = doc.select('nav a')  # Get all links within navigation elements
        
        if nav_links:
            print(f"\nFound {len(nav_links)} navigation links:")
            for i, link in enumerate(nav_links[:10]):  # Show first 10
                text = link.get_text(strip=True)
                href = link.get('href', '')
                if text and href:
                    print(f"{i+1}. {text} -> {href}")
        
        return doc
        
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None


def scrape_flatiron_courses():
    """
    Demonstrates scraping course information from Flatiron School's courses page.
    Shows how to iterate over multiple elements.
    """
    print("\n=== Scraping Flatiron School Courses ===")
    
    headers = {'user-agent': 'my-app/0.0.1'}
    
    try:
        # Scrape the courses page
        html = requests.get("https://flatironschool.com/our-courses/", headers=headers)
        html.raise_for_status()
        
        doc = BeautifulSoup(html.text, 'html.parser')
        
        # Look for course-related headings and content
        course_elements = doc.select('h2, h3, .course-title, [class*="course"]')
        
        print(f"Found {len(course_elements)} course-related elements:")
        
        courses_found = []
        for element in course_elements:
            text = element.get_text(strip=True)
            if text and len(text) > 3:  # Filter out very short text
                courses_found.append(text)
        
        # Remove duplicates while preserving order
        unique_courses = []
        for course in courses_found:
            if course not in unique_courses:
                unique_courses.append(course)
        
        for i, course in enumerate(unique_courses[:10]):  # Show first 10
            print(f"{i+1}. {course}")
            
        return doc
        
    except requests.RequestException as e:
        print(f"Error fetching courses page: {e}")
        return None


def demonstrate_beautiful_soup_methods(doc):
    """
    Demonstrates various Beautiful Soup methods and attributes.
    """
    if not doc:
        print("No document to analyze")
        return
        
    print("\n=== Beautiful Soup Methods Demonstration ===")
    
    # Find the first heading
    first_heading = doc.find('h1') or doc.find('h2') or doc.find('h3')
    
    if first_heading:
        print(f"\nFirst heading analysis:")
        print(f"Tag name: {first_heading.name}")
        print(f"Attributes: {first_heading.attrs}")
        print(f"Text content: '{first_heading.get_text(strip=True)}'")
        
        # Show parent element
        if first_heading.parent:
            print(f"Parent tag: {first_heading.parent.name}")
        
        # Show children
        children = list(first_heading.children)
        print(f"Number of children: {len(children)}")
    
    # Demonstrate different selector types
    print(f"\nSelector examples:")
    
    # Select by tag
    all_links = doc.select('a')
    print(f"Total links found: {len(all_links)}")
    
    # Select by class (if any exist)
    elements_with_class = doc.select('[class]')
    print(f"Elements with classes: {len(elements_with_class)}")
    
    # Select by id (if any exist)
    elements_with_id = doc.select('[id]')
    print(f"Elements with IDs: {len(elements_with_id)}")


def scrape_example_site():
    """
    Example of scraping a simple, reliable website for demonstration.
    Uses httpbin.org which provides testing endpoints.
    """
    print("\n=== Scraping Example Site (httpbin.org) ===")
    
    headers = {'user-agent': 'my-app/0.0.1'}
    
    try:
        # Use httpbin.org/html which returns a simple HTML page
        html = requests.get("http://httpbin.org/html", headers=headers)
        html.raise_for_status()
        
        doc = BeautifulSoup(html.text, 'html.parser')
        
        print("Successfully scraped httpbin.org/html")
        print(f"Page title: {doc.title.string if doc.title else 'No title found'}")
        
        # Extract all text from paragraphs
        paragraphs = doc.select('p')
        print(f"\nFound {len(paragraphs)} paragraphs:")
        for i, p in enumerate(paragraphs):
            text = p.get_text(strip=True)
            if text:
                print(f"{i+1}. {text}")
        
        # Extract all links
        links = doc.select('a')
        print(f"\nFound {len(links)} links:")
        for i, link in enumerate(links):
            text = link.get_text(strip=True)
            href = link.get('href', '')
            print(f"{i+1}. '{text}' -> {href}")
            
    except requests.RequestException as e:
        print(f"Error fetching example site: {e}")


def main():
    """
    Main function that demonstrates web scraping concepts.
    """
    print("Web Scraping with Beautiful Soup - Demonstration")
    print("=" * 50)
    
    # Scrape Flatiron School homepage
    doc = scrape_flatiron_homepage()
    
    # Demonstrate Beautiful Soup methods
    demonstrate_beautiful_soup_methods(doc)
    
    # Scrape courses page
    scrape_flatiron_courses()
    
    # Scrape a reliable example site
    scrape_example_site()
    
    print("\n" + "=" * 50)
    print("Scraping demonstration completed!")
    print("\nKey takeaways:")
    print("- Use requests.get() to fetch HTML content")
    print("- Use BeautifulSoup() to parse HTML into a navigable structure")
    print("- Use CSS selectors with .select() to find specific elements")
    print("- Use .get_text() to extract text content from elements")
    print("- Use .get() to extract attribute values")
    print("- Always handle potential errors with try/except blocks")


if __name__ == "__main__":
    main()
