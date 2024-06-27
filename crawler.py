import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urljoin
import os
import time

MAX_DIR_LENGTH = 50  # Maximum length of directory name
MAX_DEPTH = 3         # Maximum depth of crawling

def crawl_website(url, output_dir):
    # Truncate directory name if it exceeds maximum length
    output_dir = output_dir[:MAX_DIR_LENGTH]

    # Create output directory with user-specified name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Crawl the initial URL
    visited_urls = set()
    crawled_data = {}
    crawl_url_with_retry(url, output_dir, visited_urls, crawled_data, depth=0)

    # Check if crawled data is empty
    if not crawled_data:
        print("No data crawled. Check the crawling process.")
        return

    # Perform analysis and store results
    analyze_and_store_results(output_dir, crawled_data)

def crawl_url_with_retry(url, output_dir, visited_urls, crawled_data, depth, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            crawl_url(url, output_dir, visited_urls, crawled_data, depth)
            break  # If successful, break out of the retry loop
        except (HTTPError, URLError) as e:
            print(f"Error fetching URL {url}: {e}")
            retries += 1
            time.sleep(5)  # Add a delay before retrying
    else:
        print(f"Failed to fetch URL {url} after {max_retries} retries")

def crawl_url(url, output_dir, visited_urls, crawled_data, depth):
    if depth >= MAX_DEPTH:
        return

    if url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch webpage content
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = urlopen(req).read()
    except HTTPError as e:
        print(f"Error fetching URL {url}: {e}")
        log_error(url, f"HTTP Error: {e.code}")
        return
    except URLError as e:
        print(f"Error fetching URL {url}: {e.reason}")
        log_error(url, f"URL Error: {e.reason}")
        return
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        log_error(url, f"Error: {e}")
        return

    # Extract tags and their information
    soup = BeautifulSoup(html_content, 'html.parser')
    tags_data = {}
    for tag in soup.find_all():
        tag_name = tag.name
        tag_attributes = tag.attrs  # Fetch attributes of the tag
        tag_text = tag.text.strip() if tag.text else None  # Fetch text of the tag
        tag_info = {
            "name": tag_name,
            "attributes": tag_attributes,
            "text": tag_text
        }
        tags_data[tag_name] = tag_info

    # Store tags data along with the URL
    crawled_data[url] = {"url": url, "tags_data": tags_data}  # Include URL in the crawled data

    # Create directory for this URL
    url_directory = os.path.join(output_dir, urlparse(url).netloc)
    if not os.path.exists(url_directory):
        os.makedirs(url_directory)

    # Write tags data to JSON file
    filename = os.path.join(url_directory, urlparse(url).path.strip("/").replace("/", "_") + ".json")
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump({"url": url, "tags_data": tags_data}, json_file, ensure_ascii=False, indent=4)

    # Find and crawl links on the webpage
    for link in soup.find_all('a', href=True):
        child_url = urljoin(url, link['href'])
        crawl_url_with_retry(child_url, output_dir, visited_urls, crawled_data, depth + 1)

def log_error(url, error_message):
    error_filename = "crawl_errors.txt"
    with open(error_filename, 'a', encoding='utf-8') as file:
        file.write(f"URL: {url}\nError: {error_message}\n\n")

def analyze_and_store_results(output_dir, crawled_data):
    # Placeholder functions for calculating SEO analysis metrics
    meta_information = calculate_meta_information(crawled_data)
    page_quality = calculate_page_quality(crawled_data)
    page_structure = calculate_page_structure(crawled_data)
    link_structure = calculate_link_structure(crawled_data)
    server_info = calculate_server_info(crawled_data)
    external_factors = calculate_external_factors(crawled_data)

    # Combine all analysis results
    analysis_results = {
        "Meta information": meta_information,
        "Page quality": page_quality,
        "Page structure": page_structure,
        "Link structure": link_structure,
        "Server": server_info,
        "External factors": external_factors
    }

    # Print analysis results to console
    print("Analysis Results:")
    print("------------------")
    for aspect, score in analysis_results.items():
        print(f"{aspect}: {score}%")
    print("Analysis results:", analysis_results)
def calculate_meta_information(crawled_data):
    # Placeholder implementation for calculating Meta information score
    # Example: Count the number of meta tags with name attribute
    print("Length of crawled_data:", len(crawled_data))  # Debug statement
    meta_tag_count = 0
    if crawled_data:
        for data in crawled_data.values():
            tags_data = data.get("tags_data", {})
            for tag_info in tags_data.values():
                if tag_info["name"] == "meta" and "name" in tag_info["attributes"]:
                    meta_tag_count += 1
    
        # Score calculation based on the number of meta tags
        meta_information_score = (meta_tag_count / len(crawled_data)) * 100
        return meta_information_score
    else:
        return 0  # Return 0 if crawled_data is empty

    

def calculate_page_quality(crawled_data):
    # Placeholder implementation for calculating Page quality score
    # Example: Calculate the percentage of pages with at least one image
    pages_with_image = sum(1 for data in crawled_data.values() if any(tag_info["name"] == "img" for tag_info in data.get("tags_data", {}).values()))
    page_quality_score = (pages_with_image / len(crawled_data)) * 100
    return page_quality_score


def calculate_page_structure(crawled_data):
    # Placeholder implementation for calculating Page structure score
    # Example: Calculate the average number of headings per page
    total_headings = sum(len([tag_info for tag_info in data.get("tags_data", {}).values() if tag_info["name"].startswith("h")]) for data in crawled_data.values())
    average_headings = total_headings / len(crawled_data)
    page_structure_score = (average_headings / 6) * 100  # Assuming h1 to h6
    return page_structure_score


def calculate_link_structure(crawled_data):
    # Placeholder implementation for calculating Link structure score
    # Example: Calculate the ratio of internal to external links
    num_internal_links = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "a" and "href" in tag_info["attributes"] and urlparse(tag_info["attributes"]["href"]).netloc == urlparse(data["url"]).netloc)
    num_external_links = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "a" and "href" in tag_info["attributes"] and urlparse(tag_info["attributes"]["href"]).netloc != urlparse(data["url"]).netloc)
    total_links = num_internal_links + num_external_links
    if total_links == 0:
        return 0
    link_structure_score = (num_internal_links / total_links) * 100
    return link_structure_score


def calculate_server_info(crawled_data):
    # Placeholder implementation for calculating Server info score
    # Example: Check if the website has a meta tag with http-equiv attribute
    has_http_equiv_meta = any("meta" in tag_info["name"] and "http-equiv" in tag_info["attributes"] for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values())
    server_info_score = 100 if has_http_equiv_meta else 0
    return server_info_score


def calculate_external_factors(crawled_data):
    # Placeholder implementation for calculating External factors score
    # Example: Calculate the ratio of pages with external links
    pages_with_external_links = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "a" and "href" in tag_info["attributes"] and urlparse(tag_info["attributes"]["href"]).netloc != urlparse(data["url"]).netloc)
    external_factors_score = (pages_with_external_links / len(crawled_data)) * 100
    return external_factors_score

import os
import json

import os
import json

def load_crawled_data(output_dir):
    crawled_data = {}
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    crawled_data[data['url']] = data
    return crawled_data
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import time
import colorama

# Initialize colorama for colored output
colorama.init()

MAX_DIR_LENGTH = 50  # Maximum length of directory name
MAX_DEPTH = 3         # Maximum depth of crawling

# Function to fetch the webpage content
def fetch_page(url):
    try:
        response = requests.get(url)
        return response.text, response.status_code
    except Exception as e:
        print(colorama.Fore.RED + f"Error fetching page {url}: {e}" + colorama.Style.RESET_ALL)
        return None, None

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

# Function to analyze meta description quality
def analyze_meta_description(meta_descriptions):
    if len(meta_descriptions) == 0:
        return colorama.Fore.RED + "No meta description found." + colorama.Style.RESET_ALL
    elif len(meta_descriptions) == 1:
        return "One meta description found."
    else:
        return colorama.Fore.RED + f"{len(meta_descriptions)} meta descriptions found." + colorama.Style.RESET_ALL

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

# Function to analyze page size
def analyze_page_size(html):
    # Calculate the size of the HTML content in kB
    size_kb = len(html.encode('utf-8')) / 1024
    return size_kb

# Function to count words in the webpage content
def count_words(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Get the text from all HTML elements and count words
    text = soup.get_text()
    words = text.split()
    return len(words)

# Function to count media files
def count_media_files(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Count the number of image, audio, and video tags
    media_tags = soup.find_all(['img', 'audio', 'video'])
    return len(media_tags)

# Function to count internal and external links
def count_links(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    internal_links = []
    external_links = []
    for link in soup.find_all('a', href=True):
        parsed_link = urlparse(link['href'])
        if parsed_link.netloc == urlparse(url).netloc:
            internal_links.append(link['href'])
        else:
            external_links.append(link['href'])
    return len(internal_links), len(external_links)

# Function to crawl the website and perform SEO analysis
def crawl_and_analyze(url):
    html, status_code = fetch_page(url)
    if html:
        meta_descriptions = extract_meta_descriptions(html)
        css_file_count = count_css_files(html)
        meta_description_analysis = analyze_meta_description(meta_descriptions)
        heading_structure_analysis = analyze_heading_structure(html)
        response_time = measure_response_time(url)
        page_size = analyze_page_size(html)
        word_count = count_words(html)
        media_files_count = count_media_files(html)
        internal_links_count, external_links_count = count_links(html, url)

        print("SEO Analysis Report:")
        print(f"URL: {url}")
        if status_code != 200:
            print(colorama.Fore.RED + f"Error: HTTP Status Code {status_code}" + colorama.Style.RESET_ALL)
        print(f"Number of meta descriptions: {meta_description_analysis}")
        print(f"Number of CSS files used: {css_file_count}")
        print(f"Heading structure: {heading_structure_analysis}")
        print(f"Page response time: {response_time:.2f} seconds")
        print(f"File size: {page_size:.2f} kB")
        print(f"Words: {word_count}")
        print(f"Media files: {media_files_count}")
        print(f"Number of links: {internal_links_count} internal / {external_links_count} external")

# Main function to crawl the website and perform analysis
def main(url):
    crawl_and_analyze(url)

# Example usage
if __name__ == "__main__":
    url = "https://arthconsultancyservices.com/"  # Change this to the URL you want to analyze
    main(url)


# Example usage
#crawl_website("https://arthjobconsultancy.com", "make2")











