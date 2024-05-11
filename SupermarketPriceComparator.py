import requests
import json
import sys
sys.path.insert(0,'bs4.zip')
from bs4 import BeautifulSoup

# Imitate the Mozilla browser.
user_agent = {'User-agent': 'Mozilla/5.0'}

def compare_prices(product_laughs, product_glomark):
    # Fetching data from laughs_supermarket
    response_laughs = requests.get(product_laughs, headers=user_agent)
    soup_laughs = BeautifulSoup(response_laughs.text, 'html.parser')
    price_span_laughs = soup_laughs.find('span', {'class': 'regular-price'})
    product_name_laughs = soup_laughs.find('h1').text.strip()
    if price_span_laughs:
        price_laughs_str = price_span_laughs.text.strip()
        # Extract numerical part of the price string
        price_laughs = float(''.join(filter(str.isdigit, price_laughs_str))) / 100  # Convert to Rupees
    else:
        print("Price information not found on Laughs Supermarket website.")
        return

    # Fetching data from glomark_supermarket
    response_glomark = requests.get(product_glomark, headers=user_agent)
    soup_glomark = BeautifulSoup(response_glomark.text, 'html.parser')
    script_data = soup_glomark.find('script', {'type': 'application/ld+json'})
    if script_data:
        script_content = script_data.string.strip()
        data = json.loads(script_content)
        price_glomark = float(data['offers'][0]['price'].split('.')[0])  # Removing decimal points
        product_name_glomark = data['name']
    else:
        print("Price information not found on Glomark.lk website.")
        return

    # Print the prices
    print('Laughs  ',product_name_laughs,'Rs.: ' , price_laughs)
    print('Glomark ',product_name_glomark,'Rs.: ' , price_glomark)

    # Comparing prices
    if price_laughs > price_glomark:
        print('Glomark is cheaper Rs.:', price_laughs - price_glomark)
    elif price_laughs < price_glomark:
        print('Laughs is cheaper Rs.:', price_glomark - price_laughs)
    else:
        print('Price is the same')

laughs_coconut = 'https://scrape-sm1.github.io/site1/COCONUT%20market1super.html'
glomark_coconut = 'https://glomark.lk/coconut/p/11624'
compare_prices(laughs_coconut,glomark_coconut)

laughs_tissues = 'https://scrape-sm1.github.io/site1/FLORA%20FACIAL%20TISSUES%202%20X%20160%20BOX%20-%20HOUSEHOLD%20-%20Categories%20market1super.com.html'
glomark_tissues = 'https://glomark.lk/flora-facial-tissues-160s/p/10470'
compare_prices(laughs_tissues,glomark_tissues)

laughs_bread = 'https://scrape-sm1.github.io/site1/Crimson%20Bread%20Sliced%20market1super.com.html'
glomark_bread = 'https://glomark.lk/sandwich-bread-450g/p/13606'
compare_prices(laughs_bread,glomark_bread)