from __future__ import unicode_literals
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request

from spacy_summarization import text_summarizer
# from gensim.summarization import summarize
# from nltk_summarization import nltk_summarizer
import time
import spacy
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

# Web Scraping Pkg
# from urllib.request import urlopen


# Reading Time
def readingTime(mytext):
    total_words = len([token.text for token in nlp(mytext)])
    estimatedTime = total_words/200.0
    return estimatedTime

# # Fetch Text From Url


def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        # final_time = end-start
    return render_template('index.html', ctext=rawtext, final_summary=final_summary, final_reading_time=final_reading_time, summary_reading_time=summary_reading_time)


@app.route('/compare')
def compare():
    return render_template('compare.html')


if __name__ == '__main__':
    app.run(debug=True)
