"""
Advanced Beautiful Soup Examples
Demonstrates more specific web scraping techniques and edge cases.
"""

from bs4 import BeautifulSoup
import requests


def demonstrate_css_selectors():
    """
    Comprehensive demonstration of CSS selector usage in Beautiful Soup.
    """
    print("=== CSS Selector Examples ===")
    
    # Create sample HTML for demonstration
    sample_html = """
    <html>
        <body>
            <div id="main-content" class="container">
                <h1 class="title primary">Main Heading</h1>
                <div class="section course-info">
                    <h2 class="heading-60-black color-black mb-20">Software Engineering</h2>
                    <p class="description">Learn full-stack development</p>
                </div>
                <div class="section course-info">
                    <h2 class="heading-60-black color-black mb-20">Data Science</h2>
                    <p class="description">Master data analysis and ML</p>
                </div>
                <ul class="navigation">
                    <li><a href="/home" class="nav-link">Home</a></li>
                    <li><a href="/courses" class="nav-link active">Courses</a></li>
                    <li><a href="/about" class="nav-link">About</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    
    doc = BeautifulSoup(sample_html, 'html.parser')
    
    # 1. Select by ID
    main_content = doc.select('#main-content')
    print(f"1. Select by ID (#main-content): Found {len(main_content)} elements")
    
    # 2. Select by single class
    titles = doc.select('.title')
    print(f"2. Select by single class (.title): Found {len(titles)} elements")
    
    # 3. Select by multiple classes (all must match)
    course_headings = doc.select('.heading-60-black.color-black.mb-20')
    print(f"3. Select by multiple classes: Found {len(course_headings)} elements")
    
    # 4. Select by tag name
    all_divs = doc.select('div')
    print(f"4. Select by tag (div): Found {len(all_divs)} elements")
    
    # 5. Select by attribute
    links_with_class = doc.select('a[class]')
    print(f"5. Select by attribute (a[class]): Found {len(links_with_class)} elements")
    
    # 6. Select by attribute value
    active_links = doc.select('a[class="nav-link active"]')
    print(f"6. Select by attribute value: Found {len(active_links)} elements")
    
    # 7. Descendant selectors
    section_headings = doc.select('.section h2')
    print(f"7. Descendant selector (.section h2): Found {len(section_headings)} elements")
    
    # 8. Direct child selector
    nav_items = doc.select('.navigation > li')
    print(f"8. Direct child selector (.navigation > li): Found {len(nav_items)} elements")
    
    # Print the actual course names found
    print("\nCourse names extracted:")
    for i, heading in enumerate(course_headings, 1):
        course_name = heading.get_text(strip=True)
        print(f"  {i}. {course_name}")


def demonstrate_element_methods():
    """
    Demonstrates various methods available on Beautiful Soup elements.
    """
    print("\n=== Element Methods Demonstration ===")
    
    sample_html = """
    <div id="course-card" class="card featured" data-course-id="101">
        <h3 class="course-title">Python Programming</h3>
        <p class="description">Learn Python from <strong>scratch</strong> to advanced level.</p>
        <ul class="features">
            <li>Interactive lessons</li>
            <li>Real-world projects</li>
            <li>Expert mentorship</li>
        </ul>
        <a href="/enroll/python" class="btn btn-primary">Enroll Now</a>
    </div>
    """
    
    doc = BeautifulSoup(sample_html, 'html.parser')
    course_card = doc.select_one('#course-card')  # select_one returns first match
    
    if course_card:
        print("Course card found! Analyzing element...")
        
        # 1. Tag name
        print(f"Tag name: {course_card.name}")
        
        # 2. All attributes
        print(f"All attributes: {course_card.attrs}")
        
        # 3. Specific attribute values
        print(f"ID: {course_card.get('id')}")
        print(f"Classes: {course_card.get('class')}")
        print(f"Course ID: {course_card.get('data-course-id')}")
        
        # 4. Text content (different methods)
        print(f"All text (.get_text()): {course_card.get_text(strip=True)}")
        print(f"All text (.text): {course_card.text.strip()}")
        
        # 5. Direct string content only (no nested tags)
        strings = list(course_card.strings)
        print(f"All strings: {[s.strip() for s in strings if s.strip()]}")
        
        # 6. Find specific child elements
        title = course_card.find('h3')
        if title:
            print(f"Course title: {title.get_text(strip=True)}")
        
        # 7. Find all list items
        features = course_card.find_all('li')
        print(f"Course features:")
        for i, feature in enumerate(features, 1):
            print(f"  {i}. {feature.get_text(strip=True)}")
        
        # 8. Navigate the tree structure
        print(f"Parent element: {course_card.parent.name if course_card.parent else 'None'}")
        
        children = list(course_card.children)
        child_tags = [child for child in children if hasattr(child, 'name') and child.name]
        print(f"Child elements: {[child.name for child in child_tags]}")


def scrape_with_error_handling():
    """
    Demonstrates proper error handling when web scraping.
    """
    print("\n=== Error Handling Examples ===")
    
    urls_to_try = [
        "https://httpbin.org/html",  # Should work
        "https://httpbin.org/status/404",  # Will return 404
        "https://this-domain-does-not-exist.invalid",  # Will fail DNS lookup
    ]
    
    headers = {'user-agent': 'my-app/0.0.1'}
    
    for url in urls_to_try:
        print(f"\nTrying to scrape: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses
            
            doc = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract some basic info
            title = doc.find('title')
            title_text = title.get_text(strip=True) if title else "No title"
            
            paragraphs = doc.find_all('p')
            
            print(f"  ✅ Success! Title: '{title_text}', Paragraphs: {len(paragraphs)}")
            
        except requests.exceptions.Timeout:
            print("  ❌ Timeout - The request took too long")
            
        except requests.exceptions.ConnectionError:
            print("  ❌ Connection Error - Could not connect to the server")
            
        except requests.exceptions.HTTPError as e:
            print(f"  ❌ HTTP Error - {e}")
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request Error - {e}")
            
        except Exception as e:
            print(f"  ❌ Unexpected Error - {e}")


def demonstrate_iterating_elements():
    """
    Shows different ways to iterate over elements found by Beautiful Soup.
    """
    print("\n=== Iterating Over Elements ===")
    
    sample_html = """
    <div class="course-catalog">
        <div class="course" data-level="beginner">
            <h3>Python Basics</h3>
            <p class="duration">4 weeks</p>
            <span class="price">$299</span>
        </div>
        <div class="course" data-level="intermediate">
            <h3>Web Development</h3>
            <p class="duration">8 weeks</p>
            <span class="price">$599</span>
        </div>
        <div class="course" data-level="advanced">
            <h3>Machine Learning</h3>
            <p class="duration">12 weeks</p>
            <span class="price">$899</span>
        </div>
    </div>
    """
    
    doc = BeautifulSoup(sample_html, 'html.parser')
    
    # Find all course elements
    courses = doc.select('.course')
    print(f"Found {len(courses)} courses:")
    
    # Method 1: Simple iteration
    print("\n1. Simple iteration:")
    for i, course in enumerate(courses, 1):
        title = course.find('h3').get_text(strip=True)
        print(f"   Course {i}: {title}")
    
    # Method 2: Extract multiple pieces of data (with error handling)
    print("\n2. Detailed course information:")
    course_data = []
    
    for course in courses:
        # Always check if elements exist before accessing their properties
        title_elem = course.find('h3')
        duration_elem = course.find('.duration')
        price_elem = course.find('.price')
        
        title = title_elem.get_text(strip=True) if title_elem else "No title"
        duration = duration_elem.get_text(strip=True) if duration_elem else "Duration not specified"
        price = price_elem.get_text(strip=True) if price_elem else "Price not listed"
        level = course.get('data-level', 'Not specified')
        
        course_info = {
            'title': title,
            'duration': duration,
            'price': price,
            'level': level
        }
        course_data.append(course_info)
    
    # Display extracted data
    for course in course_data:
        print(f"   📚 {course['title']}")
        print(f"      Level: {course['level'].title()}")
        print(f"      Duration: {course['duration']}")
        print(f"      Price: {course['price']}")
        print()
    
    # Method 3: Using enumerate for numbering
    print("3. Numbered list with enumerate:")
    for index, course in enumerate(courses):
        title = course.find('h3').get_text(strip=True)
        level = course.get('data-level')
        print(f"   {index + 1}. {title} ({level})")


def main():
    """
    Run all advanced examples.
    """
    print("Advanced Beautiful Soup Examples")
    print("=" * 50)
    
    demonstrate_css_selectors()
    demonstrate_element_methods()
    scrape_with_error_handling()
    demonstrate_iterating_elements()
    
    print("\n" + "=" * 50)
    print("Advanced examples completed!")
    
    print("\nAdditional Beautiful Soup tips:")
    print("- Use .select_one() instead of .select()[0] for single elements")
    print("- Always check if elements exist before accessing their properties")
    print("- Use .get() method for attributes to avoid KeyError")
    print("- The .contents property includes text nodes and whitespace")
    print("- Use .stripped_strings for clean text iteration")
    print("- Beautiful Soup automatically handles malformed HTML")


if __name__ == "__main__":
    main()