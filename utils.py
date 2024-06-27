from django.core.mail import send_mail
from django.conf import settings
def send():
    subject="Login user"
    message="Thanks for the visit our website"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=["zainlokhdwala21@gmail.com"]
    send_mail(subject,message,from_email,recipient_list)
    
# utils.py
# utils.py

import requests
from bs4 import BeautifulSoup

def get_google_domain(country):
    if country.lower() == 'us':
        return 'https://www.google.com'
    elif country.lower() == 'india':
        return 'https://www.google.co.in'
    # Add more country-specific domains as needed

def get_search_volume(country):
    # Example function to get search volume for a country
    # You can replace this with your actual implementation
    country_search_volumes = {
        'US': '100,673,000',
        'India': '90,234,000',
        # Add more countries and their search volumes as needed
    }
    return country_search_volumes.get(country, 'Unknown')

def get_cpc(country):
    # Example function to get CPC for a country
    # You can replace this with your actual implementation
    if country.lower() == 'india':
        return '₹71.50'  # Example value in INR
    else:
        return '$1.47'  # Default example value in USD

def search_google(keyword, domain, country='US', city=None, state=None, device='DESKTOP'):
    base_url = get_google_domain(country) + '/search'
    params = {
        'q': keyword,
        'as_sitesearch': domain,
        'gl': country,
        'hl': 'en',  # Language
        'device': device
    }
    if city and state:
        params['cr'] = f'country{country}|state{state}|city{city}'
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            urls = [a['href'] for a in soup.find_all('a', href=True)]
            rank_count = sum(domain in url for url in urls)
            keyword_info = {
                'Keyword': keyword,
                'Search engine': get_google_domain(country),
                'Search volume ({})'.format(country): get_search_volume(country),
                'CPC': get_cpc(country),
                'Your rank': rank_count
            }
            return keyword_info
        else:
            print(f"Failed to fetch search results. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return None
