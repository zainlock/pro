import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

# Initialize global variables to store aggregated analysis results
total_meta_descriptions = []
total_css_files = 0
total_heading_counts = {f'h{i}': 0 for i in range(1, 7)}
total_response_time = 0
total_pages_analyzed = 0

# Function to fetch the webpage content
def fetch_page(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return None

# Function to parse the HTML and extract meta description tags
def extract_meta_descriptions(html):
    soup = BeautifulSoup(html, 'html.parser')
    meta_tags = soup.find_all('meta', attrs={'name': 'description'})
    return [tag['content'] for tag in meta_tags]

# Function to count the number of CSS files used
def count_css_files(html):
    soup = BeautifulSoup(html, 'html.parser')
    css_links = soup.find_all('link', attrs={'rel': 'stylesheet'})
    return len(css_links)

# Function to analyze heading structure
def analyze_heading_structure(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_counts = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
    return heading_counts

# Function to measure page response time
def measure_response_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return end_time - start_time

# Function to extract internal links from HTML
def extract_internal_links(html, base_url):
    internal_links = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', href=True):
        absolute_link = urljoin(base_url, link['href'])
        parsed_link = urlparse(absolute_link)
        if parsed_link.netloc == urlparse(base_url).netloc:
            internal_links.append(absolute_link)
    return internal_links

# Function to fetch CSS files from the webpage
def fetch_css_files(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        css_files = [urljoin(url, link['href']) for link in soup.find_all('link', rel='stylesheet')]
        return css_files
    except Exception as e:
        print(f"Error fetching CSS files from {url}: {e}")
        return []

# Function to analyze CSS file count and provide suggestions
def analyze_css_file_count(url):
    css_files = fetch_css_files(url)
    css_file_count = len(css_files)
    
    return css_file_count

# Function to generate SEO improvement suggestions
def generate_seo_improvement_suggestions(css_file_count, heading_structure_analysis, response_time, promote_in_social_networks):
    suggestions = []

    # Task 1: Try to reduce the number of used CSS files
    if css_file_count > 3:  # You can adjust the threshold as needed
        suggestions.append("Try to reduce the number of used CSS files to improve page loading speed. (Tip: Combine CSS files)")

    # Task 2: Review and improve the heading structure
    # You can provide specific suggestions based on the heading structure analysis
    if total_heading_counts['h1'] == 0:
        suggestions.append("Add at least one <h1> heading for better SEO. (Tip: Improve Heading Structure)")

    # Task 3: Improve the page response time
    if response_time > 3:  # You can adjust the threshold as needed
        suggestions.append("Optimize page elements and server performance to improve response time. (Tip: Optimize Page)")

    # Task 4: Promote your page in social networks
    if promote_in_social_networks:
        suggestions.append("Promote your page on social networks to increase visibility and traffic. (Tip: Promote on Social Networks)")

    return suggestions

# Function to perform SEO analysis for a website
def seo_analysis(url):
    global total_meta_descriptions, total_css_files, total_heading_counts, total_response_time, total_pages_analyzed

    visited_urls = set()

    def crawl_and_analyze(url):
        global total_css_files, total_response_time, total_pages_analyzed

        if url in visited_urls:
            return
        visited_urls.add(url)

        print(f"Analyzing page: {url}")
        html = fetch_page(url)
        if html:
            meta_descriptions = extract_meta_descriptions(html)
            total_meta_descriptions.extend(meta_descriptions)
            total_css_files += count_css_files(html)
            heading_structure_analysis = analyze_heading_structure(html)
            for tag, count in heading_structure_analysis.items():
                total_heading_counts[tag] += count
            total_response_time += measure_response_time(url)
            total_pages_analyzed += 1

            internal_links = extract_internal_links(html, url)
            for link in internal_links:
                crawl_and_analyze(link)

    crawl_and_analyze(url)

    # Analyze CSS file count and provide suggestions
    css_file_count = analyze_css_file_count(url)
    css_suggestions = generate_seo_improvement_suggestions(css_file_count, total_heading_counts, total_response_time, True)

    # Print aggregated results including CSS suggestions
    print("\nSEO Analysis Report:")
    print(f"Total pages analyzed: {total_pages_analyzed}")
    print(f"Total meta descriptions found: {len(total_meta_descriptions)}")
    print(f"Total CSS files used: {total_css_files}")
    print("Total heading structure:")
    for tag, count in total_heading_counts.items():
        print(f"{tag}: {count}")
    print(f"Total response time: {total_response_time} seconds")
    print("Suggestions:")
    suggestions = generate_seo_improvement_suggestions(
        css_file_count, total_heading_counts, total_response_time, True
    )

    # Print the suggestions
    print("SEO Improvement Suggestions:")
    for suggestion in suggestions:
        print(suggestion)

# Example usage
url = "https://arthjobconsultancy.com"  # Change this to the URL you want to analyze
seo_analysis(url)
