import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize FLAN-T5 model
tokenizer = AutoTokenizer.from_pretrained("t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

def summarize_text(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model.generate(inputs.input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4)
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

def build_search_query(form_data):
    """
    Constructs an arXiv search query string from form data.
    
    Args:
        form_data (dict): Dictionary containing form input fields.

    Returns:
        str: Search query for arXiv.
    """
    query_parts = []

    # Regular search query
    if form_data.get("query"):
        query_parts.append(f"all:{form_data['query']}")

    # Author field
    if form_data.get("author"):
        query_parts.append(f"author:{form_data['author']}")

    # Organization field
    if form_data.get("organization"):
        query_parts.append(f"affil:{form_data['organization']}")

    # Date range
    if form_data.get("published_from") and form_data.get("published_to"):
        query_parts.append(f"submittedDate:[{form_data['published_from']} TO {form_data['published_to']}]")

    # Keywords field
    if form_data.get("keywords"):
        query_parts.append(f"abs:{form_data['keywords']}")

    # Combine all parts with AND
    query = " AND ".join(query_parts)
    print(f"Generated search query: {query}")  # Debugging statement
    return query

import requests
from xml.etree import ElementTree

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_papers(query, search_field):
    # Build the search query
    query_param = f"{search_field}:{query}" if search_field != "all" else query
    url = f"{ARXIV_API_URL}?search_query={query_param}&start=0&max_results=5"

    response = requests.get(url)
    response.raise_for_status()

    return parse_arxiv_response(response.text)

def parse_arxiv_response(response_text):
    root = ElementTree.fromstring(response_text)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        paper = {
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
            "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
            "authors": ", ".join(
                author.find("{http://www.w3.org/2005/Atom}name").text
                for author in entry.findall("{http://www.w3.org/2005/Atom}author")
            ),
            "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
            "id": entry.find("{http://www.w3.org/2005/Atom}id").text,
        }
        papers.append(paper)

    return papers