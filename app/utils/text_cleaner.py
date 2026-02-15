import re


def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    # remove weird symbols
    text = re.sub(r'[^\w\s.,%-]', '', text)

    return text.strip()
