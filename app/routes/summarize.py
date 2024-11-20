from flask import Blueprint, request, jsonify
from transformers import pipeline

summarize_blueprint = Blueprint('summarize', __name__)

# Use BART for summarization (better suited for longer texts)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    if len(text.split()) < 30:
        return text  # Skip summarization for very short text
    # Use BART for generating a more accurate summary
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]["summary_text"]