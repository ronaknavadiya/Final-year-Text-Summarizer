from __future__ import unicode_literals
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from nltk_summarization import nltk_summarizer
from gensim.summarization import summarize
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request
from main_summary import main_summary
import requests
import re

from spacy_summarization import text_summarizer
import time
import spacy
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

# Sumy


def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

# Reading Time


def readingTime(mytext):
    total_words = len([token.text for token in nlp(mytext)])
    estimatedTime = total_words/200.0
    return estimatedTime

# # Fetch Text From Url


def get_text(url):
    def getdata(url):
        r = requests.get(url)
        return r.text

    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    finalText = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    # removing refrence tag
    finalText = re.sub(r"\[.*?\]+", '', finalText)
    finalText = finalText.replace('\n', '')[:-11]
    return finalText


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary = main_summary(rawtext)
        summary_reading_time = readingTime(final_summary)
        spacy_words = len(final_summary.split())
        ctext_words = len(rawtext.split())
    return render_template('index.html', ctext_words=ctext_words, spacy_words=spacy_words, ctext=rawtext, final_summary=final_summary, final_reading_time=final_reading_time, summary_reading_time=summary_reading_time)


@app.route('/compare')
def compare():
    return render_template('compare.html')


@app.route('/analyze_url', methods=['GET', 'POST'])
def analyze_url():
    if request.method == 'POST':
        try:
            raw_url = request.form['raw_url']
        except urllib.error.URLError as e:
            ResponseData = e.reason
            print("error:", ResponseData)

        rawtext = get_text(raw_url)

        final_reading_time = readingTime(rawtext)
        final_summary = main_summary(rawtext)
        summary_reading_time = readingTime(final_summary)
        spacy_words = len(final_summary.split())
        ctext_words = len(rawtext.split())
    return render_template('index.html', ctext_words=ctext_words, spacy_words=spacy_words, final_summary=final_summary, summary_reading_time=summary_reading_time, ctext=rawtext, final_reading_time=final_reading_time,)


@app.route('/analyze_compare_url', methods=['GET', 'POST'])
def analyze_compare_url():
    try:
        raw_url = request.form['raw_url']
    except urllib.error.URLError as e:
        ResponseData = e.reason
        print("error:", ResponseData)
    rawtext = get_text(raw_url)
    # Spacy Summarizer
    final_summary_spacy = text_summarizer(rawtext)
    summary_reading_time = readingTime(final_summary_spacy)
    spacy_words = len(final_summary_spacy.split())
    # Gensim Summarizer
    final_summary_gensim = summarize(rawtext)
    summary_reading_time_gensim = readingTime(final_summary_gensim)
    genism_words = len(final_summary_gensim.split())
    # page_rank
    final_summary_page_rank = main_summary(rawtext)
    summary_reading_time_page_rank = readingTime(final_summary_page_rank)
    page_rank_words = len(final_summary_page_rank.split())
    # Sumy
    final_summary_sumy = sumy_summary(rawtext)
    summary_reading_time_sumy = readingTime(final_summary_sumy)
    sumy_words = len(final_summary_sumy.split())

    return render_template('compare.html', spacy_words=spacy_words, genism_words=genism_words, page_rank_words=page_rank_words, sumy_words=sumy_words, final_summary_spacy=final_summary_spacy, final_summary_gensim=final_summary_gensim, final_summary_page_rank=final_summary_page_rank,  final_summary_sumy=final_summary_sumy, summary_reading_time=summary_reading_time, summary_reading_time_gensim=summary_reading_time_gensim, summary_reading_time_sumy=summary_reading_time_sumy, summary_reading_time_page_rank=summary_reading_time_page_rank)


@app.route('/comparer', methods=['GET', 'POST'])
def comparer():

    if request.method == 'POST':
        rawtext = request.form['rawtext']
        # Spacy
        final_summary_spacy = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary_spacy)
        spacy_words = len(final_summary_spacy.split())
        # Gensim Summarizer
        final_summary_gensim = summarize(rawtext)
        summary_reading_time_gensim = readingTime(final_summary_gensim)
        genism_words = len(final_summary_gensim.split())
        # page_rank
        final_summary_page_rank = main_summary(rawtext)
        summary_reading_time_page_rank = readingTime(final_summary_page_rank)
        page_rank_words = len(final_summary_page_rank.split())
        # Sumy
        final_summary_sumy = sumy_summary(rawtext)
        summary_reading_time_sumy = readingTime(final_summary_sumy)
        sumy_words = len(final_summary_sumy.split())

    return render_template('compare.html', spacy_words=spacy_words, genism_words=genism_words, page_rank_words=page_rank_words, sumy_words=sumy_words, final_summary_spacy=final_summary_spacy, final_summary_gensim=final_summary_gensim, final_summary_page_rank=final_summary_page_rank,  final_summary_sumy=final_summary_sumy, summary_reading_time=summary_reading_time, summary_reading_time_gensim=summary_reading_time_gensim, summary_reading_time_sumy=summary_reading_time_sumy, summary_reading_time_page_rank=summary_reading_time_page_rank)


if __name__ == '__main__':
    app.run(debug=True)
