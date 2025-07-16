import json
from datetime import datetime
from googletrans import Translator
from googleapiclient.discovery import build
from newspaper import Article

def google_search(query, api_key, cse_id, num_results=1): 

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
        return res.get("items", [])
    except Exception as e:
        print(f"Error during Google search for '{query}': {e}")
        return []

def extract_blog_content(url):

    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "url": url,
            "authors": article.authors,
            "publish_date": str(article.publish_date) if article.publish_date else None
        }
    except Exception as e:
        print(f"Error extracting blog content from {url}: {e}")
        return {}

def main():
    GOOGLE_API_KEY = ""
    CSE_ID = ""
    
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data.json: {e}")
        return
    
    translator = Translator()

    now = datetime.now()
    current_date = f"{now.month}/{now.day}/{now.year}"

    countries_trending_blog = {}

    for country, details in data.get("Country_trends", {}).items():
        trends = details.get("trends", [])
        if not trends:
            print(f"[{country}] No trends available.")
            countries_trending_blog[country] = {"date": current_date}
            continue
        
        country_blog_data = {"date": current_date}
        for t_index, trend in enumerate(trends[:10], start=1):
            detected = translator.detect(trend)
            if detected.lang != 'en':
                trend_en = translator.translate(trend, dest='en').text
            else:
                trend_en = trend
            
            print(f"[{country}] Processing trend {t_index}: '{trend_en}'")
            query = f"best blog about {trend_en}"
            search_results = google_search(query, GOOGLE_API_KEY, CSE_ID, num_results=1)

            trend_blog = {"trend": trend_en}
            for b_index, item in enumerate(search_results, start=1):
                blog_url = item.get("link")
                print(f"    Trend {t_index} → Blog {b_index} URL: {blog_url}")
                blog_content = extract_blog_content(blog_url)
                trend_blog[f"bg{b_index}"] = blog_content
            country_blog_data[f"blog{t_index}"] = trend_blog
        
        countries_trending_blog[country] = country_blog_data

    data["Countries_trending_Blog"] = countries_trending_blog

    try:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Blog content saved to data.json under 'Countries_trending_Blog'.")
    except Exception as e:
        print(f"Error saving data.json: {e}")

if __name__ == "__main__":
    main()
