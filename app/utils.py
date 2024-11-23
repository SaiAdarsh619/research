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

def fetch_papers(query, field):
    # Build the correct search query
    field_map = {
        "all": "all",
        "title": "ti",
        "author": "au",
        "abstract": "abs",
    }
    search_field = field_map.get(field, "all")
    search_query = f"{search_field}:{query}"

    # ArXiv API URL
    arxiv_url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results=10"

    response = requests.get(arxiv_url)
    response.raise_for_status()

    # Parse response
    root = ElementTree.fromstring(response.text)
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        paper_id = entry.find("{http://www.w3.org/2005/Atom}id").text.split("/")[-1]
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
        authors = [
            author.find("{http://www.w3.org/2005/Atom}name").text.strip()
            for author in entry.findall("{http://www.w3.org/2005/Atom}author")
        ]
        published = entry.find("{http://www.w3.org/2005/Atom}published").text

        papers.append({
            "id": paper_id,
            "title": title,
            "summary": summary,
            "authors": ", ".join(authors),
            "published": published,
        })

    return papers
def parse_arxiv_response(response_text):
    from xml.etree import ElementTree

    root = ElementTree.fromstring(response_text)
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        author_elems = entry.findall("{http://www.w3.org/2005/Atom}author")
        authors = ", ".join(a.find("{http://www.w3.org/2005/Atom}name").text for a in author_elems if a.find("{http://www.w3.org/2005/Atom}name") is not None)
        organization = entry.find("{http://www.w3.org/2005/Atom}arxiv:affiliation", namespaces={"arxiv": "http://arxiv.org/schemas/atom"})
        organization = organization.text if organization is not None else "Unknown Organization"

        # Extract the arXiv ID from the entry's id tag
        arxiv_id = entry.find("{http://www.w3.org/2005/Atom}id").text.split('/')[-1]  # This should extract the unique identifier (e.g., 1234.5678)

        papers.append({
            "title": title,
            "summary": None,  # Placeholder for batch summarization
            "authors": authors,
            "published": published,
            "organization": organization,
            "id": arxiv_id  # Store the extracted arXiv ID here
        })

    # Summarize in batch
    summaries = summarize_text([paper['summary'] for paper in papers])
    for paper, summary in zip(papers, summaries):
        paper['summary'] = summary

    return papers
