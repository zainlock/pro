from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urljoin
import time

MAX_DEPTH = 3 

def crawl_websites(url, keyword):
    visited_urls = set()
    keyword_occurrences = {}

    crawl_url_with_retry(url, visited_urls, keyword_occurrences, keyword, depth=0)

    return keyword_occurrences

def crawl_url_with_retry(url, visited_urls, keyword_occurrences, keyword, depth, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            crawl_urls(url, visited_urls, keyword_occurrences, keyword, depth)
            break  # If successful, break out of the retry loop
        except (HTTPError, URLError) as e:
            print(f"Error fetching URL {url}: {e}")
            retries += 1
            time.sleep(5)  # Add a delay before retrying
    else:
        print(f"Failed to fetch URL {url} after {max_retries} retries")

def crawl_urls(url, visited_urls, keyword_occurrences, keyword, depth):
    if depth >=MAX_DEPTH:
        return

    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = urlopen(req).read()
    except (HTTPError, URLError) as e:
        print(f"Error fetching URL {url}: {e}")
        return
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()

    occurrences = text_content.lower().count(keyword.lower())
    if occurrences > 0:
        keyword_occurrences[url] = occurrences

    for link in soup.find_all('a', href=True):
        child_url = urljoin(url, link['href'])
        crawl_url_with_retry(child_url, visited_urls, keyword_occurrences, keyword, depth + 1)

# Main function
if __name__ == "__main__":
    # User input: Keyword to search
    keyword = input("Enter keyword to search: ")

    # User input: Base URL of the website to search
    base_url = input("Enter base URL of the website to search: ")

    # Crawl the website and count keyword occurrences
    keyword_occurrences = crawl_websites(base_url, keyword)

    # Print keyword occurrences
    print(f"Keyword '{keyword}' occurrences across the website:")
    for url, occurrences in keyword_occurrences.items():
        print(f"{url}: {occurrences} occurrences")
