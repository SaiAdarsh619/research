import subprocess
import json
from transformers import pipeline

# Initialize summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_kaggle_datasets(query):
    """
    Fetches Kaggle datasets based on a query using the Kaggle API.
    """
    try:
        # Use the Kaggle CLI to search datasets
        result = subprocess.run(
            ['kaggle', 'datasets', 'list', '-s', query, '--json'],
            capture_output=True, text=True
        )
        
        # Parse JSON response
        datasets = json.loads(result.stdout)
        return [
            {
                "title": dataset["title"],
                "description": dataset["subtitle"],
                "link": f'https://www.kaggle.com/{dataset["ref"]}'
            }
            for dataset in datasets
        ]
    except Exception as e:
        print(f"Error fetching Kaggle datasets: {e}")
        return []

def summarize_text(text):
    """
    Summarizes text using a transformer-based summarizer.
    """
    if len(text.split()) < 30:
        return text  # Skip summarization for very short text
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
