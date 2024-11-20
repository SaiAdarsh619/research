import requests
from transformers import pipeline

# Initialize summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_papers(query):
    arxiv_url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5'

    try:
        response = requests.get(arxiv_url)
        response.raise_for_status()  # Ensure the request was successful

        if response.status_code == 200:
            papers = parse_arxiv_response(response.text)
            return papers
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching papers: {e}")
        return []

def parse_arxiv_response(response_text):
    from xml.etree import ElementTree

    root = ElementTree.fromstring(response_text)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        # Extract title
        title = entry.find("{http://www.w3.org/2005/Atom}title").text or "No title available"

        # Extract summary
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text or "No summary available"

        # Extract authors
        authors = entry.findall("{http://www.w3.org/2005/Atom}author")
        author_names = [author.find("{http://www.w3.org/2005/Atom}name").text for author in authors if author is not None]
        author_names = ', '.join(author_names) if author_names else "Unknown authors"

        # Extract published date
        published = entry.find("{http://www.w3.org/2005/Atom}published")
        published_date = published.text if published is not None else "Unknown publication date"

        # Extract affiliations (organizations) if available
        affiliations = []
        for author in authors:
            affiliation = author.find("{http://arxiv.org/schemas/atom}affiliation")
            if affiliation is not None:
                affiliations.append(affiliation.text)
        organization = ', '.join(affiliations) if affiliations else "Unknown organization"

        papers.append({
            "title": title,
            "summary": summarize_text(summary),  # Summarize using the enhanced summarizer
            "authors": author_names,
            "organization": organization,
            "published_date": published_date,
        })

    return papers

def summarize_text(text):
    if len(text.split()) < 30:
        return text  # Skip summarization for very short text
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]["summary_text"]
