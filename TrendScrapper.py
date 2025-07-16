import json
from datetime import datetime
import time
import requests
from pytrends.request import TrendReq
from googletrans import Translator


def get_google_nid_cookie():
    session = requests.Session()
    try:
        session.get('https://trends.google.com', timeout=10)
        cookies_map = session.cookies.get_dict()
        return cookies_map.get('NID', '')
    except Exception as e:
        print(f"Error fetching NID cookie: {e}")
        return ''

def get_country_trends(pn, top_n=10):
    try:
        nid_cookie = get_google_nid_cookie()
        # Create TrendReq object with the cookie if available
        pytrends = TrendReq(hl='en-US', tz=360, requests_args={'headers': {'Cookie': f'NID={nid_cookie}'}})
        trending_data = pytrends.today_searches(pn=pn)
        
        if trending_data is not None and not trending_data.empty:
            all_trends = []
            for col in trending_data.columns:
                all_trends.extend(trending_data[col].tolist())
            # Remove duplicates while preserving order
            all_trends = list(dict.fromkeys(all_trends))
            return [trend for trend in all_trends if trend is not None][:top_n]
        else:
            return []
    except Exception as e:
        print(f"Error retrieving trends for {pn}: {e}")
        return []

def translate_trend(trend, translator):
    try:
        detection = translator.detect(trend)
        if detection.lang != 'en':
            translation = translator.translate(trend, dest='en')
            return translation.text
        else:
            return trend
    except Exception as e:
        print(f"Error translating trend '{trend}': {e}")
        return trend

def main():
    # Updated country codes using ISO two-letter codes
    country_codes = {
        "USA": "US",
        "China": "CN",      
        "India": "IN",
        "Japan": "JP",
        "Pakistan": "PK", 
        "Canada": "CA",
        "Australia": "AU",
        "England": "GB",
        "Turkey": "TR",
        "Germany": "DE"
    }
    
    now = datetime.now()
    current_date = f"{now.month}/{now.day}/{now.year}"
    
    translator = Translator()
    country_trends = {}
    
    for country, code in country_codes.items():
        trends = get_country_trends(pn=code, top_n=10)
        translated_trends = [translate_trend(trend, translator) for trend in trends]
        country_trends[country] = {
            "date": current_date,
            "trends": translated_trends
        }

    final_data = {"Country_trends": country_trends}
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
    
    print("Trends saved to data.json")

if __name__ == "__main__":
    main()

