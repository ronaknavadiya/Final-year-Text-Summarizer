from __future__ import unicode_literals
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from nltk_summarization import nltk_summarizer
from gensim.summarization import summarize
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request

from spacy_summarization import text_summarizer
import time
import spacy
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)


# from __future__ import unicode_literals
# from flask import Flask,render_template,url_for,request

# from spacy_summarization import text_summarizer
# import time
# import spacy
# nlp = spacy.load('en_core_web_sm')
# app = Flask(__name__)

# # Web Scraping Pkg
# from bs4 import BeautifulSoup
# # from urllib.request import urlopen
# from urllib.request import urlopen

# Sumy Pkg

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


@app.route('/analyze_url', methods=['GET', 'POST'])
def analyze_url():
    start = time.time()
    if request.method == 'POST':
        try:
            raw_url = request.form['raw_url']
        except urlopen.error.URLError as e:
            ResponseData = e.read().decode("utf8", 'ignore')
            print("error:", ResponseData)
        rawtext = get_text(raw_url)
        final_reading_time = readingTime(rawtext)
        final_summary = summarize(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end-start
    return render_template('index.html', final_summary=final_summary, summary_reading_time=summary_reading_time, ctext=rawtext, final_reading_time=final_reading_time,)


@app.route('/analyze_compare_url', methods=['GET', 'POST'])
def analyze_compare_url():
    raw_url = request.form['raw_url']
    rawtext = get_text(raw_url)
    # Spacy Summarizer
    final_reading_time = readingTime(rawtext)
    final_summary_spacy = text_summarizer(rawtext)
    summary_reading_time = readingTime(final_summary_spacy)
    spacy_words = len(final_summary_spacy.split())
    # Gensim Summarizer
    final_summary_gensim = summarize(rawtext)
    summary_reading_time_gensim = readingTime(final_summary_gensim)
    genism_words = len(final_summary_gensim.split())
    # NLTK
    final_summary_nltk = nltk_summarizer(rawtext)
    summary_reading_time_nltk = readingTime(final_summary_nltk)
    nltk_words = len(final_summary_nltk.split())
    # Sumy
    final_summary_sumy = sumy_summary(rawtext)
    summary_reading_time_sumy = readingTime(final_summary_sumy)
    sumy_words = len(final_summary_sumy.split())

    return render_template('compare.html', spacy_words=spacy_words, genism_words=genism_words, nltk_words=nltk_words, sumy_words=sumy_words, final_summary_spacy=final_summary_spacy, final_summary_gensim=final_summary_gensim, final_summary_nltk=final_summary_nltk,  final_summary_sumy=final_summary_sumy, summary_reading_time=summary_reading_time, summary_reading_time_gensim=summary_reading_time_gensim, summary_reading_time_sumy=summary_reading_time_sumy, summary_reading_time_nltk=summary_reading_time_nltk)


@app.route('/comparer', methods=['GET', 'POST'])
def comparer():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary_spacy = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary_spacy)
        spacy_words = len(final_summary_spacy.split())
        # Gensim Summarizer
        final_summary_gensim = summarize(rawtext)
        summary_reading_time_gensim = readingTime(final_summary_gensim)
        genism_words = len(final_summary_gensim.split())
        # NLTK
        final_summary_nltk = nltk_summarizer(rawtext)
        summary_reading_time_nltk = readingTime(final_summary_nltk)
        nltk_words = len(final_summary_nltk.split())
        # Sumy
        final_summary_sumy = sumy_summary(rawtext)
        summary_reading_time_sumy = readingTime(final_summary_sumy)
        sumy_words = len(final_summary_sumy.split())

        end = time.time()
        final_time = end-start
    return render_template('compare.html', spacy_words=spacy_words, genism_words=genism_words, nltk_words=nltk_words, sumy_words=sumy_words, final_summary_spacy=final_summary_spacy, final_summary_gensim=final_summary_gensim, final_summary_nltk=final_summary_nltk,  final_summary_sumy=final_summary_sumy, summary_reading_time=summary_reading_time, summary_reading_time_gensim=summary_reading_time_gensim, summary_reading_time_sumy=summary_reading_time_sumy, summary_reading_time_nltk=summary_reading_time_nltk)


if __name__ == '__main__':
    app.run(debug=True)
