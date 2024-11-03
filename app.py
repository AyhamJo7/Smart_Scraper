import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import json
import subprocess
from datetime import datetime


def scrape_data(url):
    load_dotenv()
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    scraped_data = app.scrape_url(url)
    if 'markdown' in scraped_data:
        return scraped_data['markdown']
    else:
        raise KeyError("The key 'markdown' does not exist in the scraped data.")

def save_raw_data(raw_data, timestamp, url, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    raw_output_path = os.path.join(output_folder, f'rawData_{safe_url}_{timestamp}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(raw_data)
    print(f"Raw data saved to {raw_output_path}")

def format_data(data, fields=None):
    load_dotenv()
    if fields is None:
        fields = ["Name", "Pricing", "Description", "Hashtags"]
    system_message = f"""You are an intelligent text extraction assistant. Your task is to extract structured information about AI tools from the provided markdown text. The markdown contains a list of AI tools, each with its Name, Pricing, Description, and Hashtags. Extract these fields for each tool and return the data in a JSON array format."""
    user_message = f"Extract the structured data from the following text:\n\n{data}"
    ollama_path = "C:\\Users\\ayham\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
    command = [ollama_path, "run", "llama3.2"]
    try:
        input_text = f"{system_message}\n\n{user_message}"
        result = subprocess.run(
            command,
            input=input_text,
            capture_output=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        formatted_data = result.stdout.strip()
        try:
            parsed_json = json.loads(formatted_data)
            return parsed_json
        except json.JSONDecodeError:
            print(f"JSON decoding error: {formatted_data}")
            raise ValueError("Failed to parse JSON output.")
    except Exception as e:
        print(f"Error: {e}")
        raise

def save_formatted_data(formatted_data, timestamp, url, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    output_path = os.path.join(output_folder, f'sorted_data_{safe_url}_{timestamp}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Formatted data saved to {output_path}")

if __name__ == "__main__":
    urls = [
        'https://www.futurepedia.io/ai-tools/research-assistant',
        'https://www.futurepedia.io/ai-tools/personal-assistant'
    ]
    for url in urls:
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_data = scrape_data(url)
            save_raw_data(raw_data, timestamp, url)
            formatted_data = format_data(raw_data)
            save_formatted_data(formatted_data, timestamp, url)
        except Exception as e:
            print(f"An error occurred for {url}: {e}")
