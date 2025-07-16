import json
import time
from datetime import datetime
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="together",
    api_key=""
)

def deepseek_summarize_single(text, model="deepseek-ai/DeepSeek-R1", retries=3):

    prompt = (
        "Summarize the following blog content into a coherent, well-structured article summary limited to exact 1500 characters.This article should be well explained focus on main points "
        " Do not include extra text.\n\n"
        "Blog Content:\n" + text
    )
    messages = [{"role": "user", "content": prompt}]
    attempt = 0
    while attempt < retries:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
            )
            output_text = completion.choices[0].message.content.strip()
            try:
                result_json = json.loads(output_text)
                if "Article" in result_json:
                    return result_json
                else:
                    print("JSON output missing 'Article' key. Raw output:")
                    print(output_text)
                    return {"Article": output_text}
            except json.JSONDecodeError:
                print("Failed to decode JSON from model output. Raw output:")
                print(output_text)
                return {"Article": output_text}
        except Exception as e:
            print(f"DeepSeek summarization error (attempt {attempt+1}): {e}")
            attempt += 1
            time.sleep(2)
    return {"Article": "Error in summarization."}

def robust_deepseek_summarize(text, max_chunk=800):

    if len(text) <= max_chunk:
        return deepseek_summarize_single(text)
    
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    chunk_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {idx}/{len(chunks)}...")
        summary_dict = deepseek_summarize_single(chunk)
        chunk_text = summary_dict.get("Article", "")
        chunk_summaries.append(chunk_text)
        time.sleep(1)
    combined_summary_text = "\n".join(chunk_summaries)
    print("Summarizing combined chunk summaries...")
    final_summary = deepseek_summarize_single(combined_summary_text)
    return final_summary

def main():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data.json: {e}")
        return

    countries_blog = data.get("Countries_trending_Blog", {})
    now = datetime.now()
    current_date = f"{now.month}/{now.day}/{now.year}"

    blog_articles = {}

    for country, details in countries_blog.items():
        print(f"Processing country: {country}")
        country_articles = {"date": details.get("date", current_date)}
        for i in range(1, 11):
            blog_key = f"blog{i}"
            blog_group = details.get(blog_key, {})
            if not blog_group:
                print(f"  [{country}] No data for {blog_key}")
                continue
            combined_text = ""

            for j in range(1, 11):
                bg_key = f"bg{j}"
                blog_item = blog_group.get(bg_key, {})
                if blog_item and "text" in blog_item:
                    combined_text += blog_item["text"] + "\n"
            if not combined_text.strip():
                print(f"  [{country}] No blog content for {blog_key}")
                continue
            summary = robust_deepseek_summarize(combined_text)
            print(f"  [{country}] Summary for {blog_key} obtained.")
            country_articles[blog_key] = summary
        blog_articles[country] = country_articles

    final_output = {"Countries_Blog_Articles": blog_articles}

    try:
        with open("blog_articles.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4, ensure_ascii=False)
        print("Blog articles saved to blog_articles.json")
    except Exception as e:
        print(f"Error saving blog_articles.json: {e}")

if __name__ == "__main__":
    main()
