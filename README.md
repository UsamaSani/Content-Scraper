# 🌐 AI-Powered Trend Blog Generator

A Python-based project that scrapes real-time trending topics from Google Trends, retrieves top blog articles, translates them (if needed), and generates concise, custom-written summaries using powerful AI models like DeepSeek and LLaMA.

---

## 🚀 Features

* 🔍 **Trend Scraping**: Fetches today's top trending search terms for multiple countries using `pytrends`.
* 🌍 **Language Translation**: Automatically detects and translates non-English trends and blog content into English using `googletrans`.
* 📰 **Content Scraping**: Searches for blog articles using the Google Custom Search API and extracts their content via `newspaper3k`.
* 🤖 **AI Content Generation**: Summarizes blog content using state-of-the-art large language models like **DeepSeek-R1** (via HuggingFace).
* 📀 **Structured Output**: All results are stored in structured JSON files (`data.json` and `blog_articles.json`).

---

## 📁 Project Structure

```bash
🔺 trendscraper.py       # Scrapes top Google Trends for selected countries
🔺 blogscraper.py        # Searches and extracts blog content based on trends
🔺 llm.py                # Uses DeepSeek/LLaMA to generate custom article summaries
🔺 data.json             # Stores trends and raw blog data
🔺 blog_articles.json    # Stores final summarized articles
🔺 README.md             # Project documentation
```

---

## 🌍 Supported Countries

* 🇺🇸 USA
* 🇨🇳 China
* 🇮🇳 India
* 🇵🇰 Pakistan
* 🇬🇧 England
* 🇨🇦 Canada
* 🇩🇪 Germany
* 🇯🇵 Japan
* 🇹🇷 Turkey
* 🇦🇺 Australia

---

## 🧐 Technologies Used

| Tool/Library        | Purpose                           |
| ------------------- | --------------------------------- |
| `pytrends`          | Fetch Google Trends               |
| `googletrans`       | Translate text to English         |
| `newspaper3k`       | Extract content from article URLs |
| `googleapiclient`   | Perform Google Custom Search      |
| `huggingface_hub`   | Call DeepSeek/LLM models via API  |
| `json` / `datetime` | Handle data and formatting        |

---

## 🔧 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/UsamaSani/Content-Scraper.git
   cd Content-Scraper
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add API Keys**

   * Replace placeholders in:

     * `llm.py` → `api_key` for HuggingFace or Together API
     * `blogscraper.py` → `GOOGLE_API_KEY` and `CSE_ID` for Google Custom Search Engine

4. **Run the Scripts**

   ```bash
   python trendscraper.py      # Step 1: Fetch trending topics
   python blogscraper.py       # Step 2: Scrape blog content
   python llm.py               # Step 3: Generate AI-powered summaries
   ```

---

## 📌 Example Output (JSON)

### `data.json`

```json
{
  "Country_trends": {
    "USA": {
      "date": "7/16/2025",
      "trends": ["Taylor Swift", "OpenAI GPT-5", ...]
    },
    ...
  }
}
```

### `blog_articles.json`

```json
{
  "Countries_Blog_Articles": {
    "USA": {
      "blog1": {
        "Article": "Taylor Swift just released a..."
      },
      ...
    }
  }
}
```

---

## 🔬 Use Cases

* 🔥 Trend-based blogging and SEO content generation
* 🌐 Market analysis and localization
* ✍️ Automated news/blog summarization
* 📊 AI content pipelines for research or journalism

---

## 📃 License

This project is licensed under the **MIT License**. Feel free to use and adapt it.

---

## 🤛🏼 Author

**Usama Sani Khanzada**
[🔗 Portfolio Website](https://www.usamasani.tech)
[👨‍💼 GitHub](https://github.com/UsamaSani) • [💼 LinkedIn](https://www.linkedin.com/in/usama-sani-khanzada-5b6552240/)

---

> 💡 Want to contribute or improve the project? Feel free to fork and open a pull request!
