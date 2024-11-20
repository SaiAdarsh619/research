from flask import Blueprint, request, jsonify
from transformers import pipeline

summarize_blueprint = Blueprint('summarize', __name__)

# Initialize summarizer with a specific model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@summarize_blueprint.route("/", methods=["POST"])
def summarize_text(text):
    word_count = len(text.split())
    
    # Set dynamic max_length based on input length
    max_len = min(150, word_count - 1)  # Ensure max_length is shorter than input
    min_len = max(40, int(0.3 * word_count))  # Dynamic min_length as 30% of input length

    if word_count < 30:  # Skip summarization for very short text
        return text

    try:
        summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Error during summarization: {e}")
        return text  # Return original text if summarization fails
