import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import warnings
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')

def home():
    return render_template('input.html')


@app.route('/summarize', methods=['POST'])
# warnings.filterwarnings('ignore')
# f = open('input1.txt', 'r', errors='ignore')
# text = f.read()
def summarize():
    text = request.form['text']
    stopwords = list(STOP_WORDS)
    # print(stopwords)

    spacy.cli.download("en")
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    tokens = [token.text for token in doc]
    # print(tokens)
    from string import punctuation
    punctuation = punctuation + '\n'
    # print(punctuation)

    word_freqencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_freqencies.keys():
                    word_freqencies[word.text] = 1
                else:
                    word_freqencies[word.text] += 1
    # print(word_frequencies)

    max_frequency = max(word_freqencies.values())
    # print(max_frequency)

    for word in word_freqencies.keys():
        word_freqencies[word] = word_freqencies[word] / max_frequency
    # print(word_freqencies)

    sentence_tokens = [sent for sent in doc.sents]
    # print(sentence_tokens)

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_freqencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_freqencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_freqencies[word.text.lower()]

    # print(sentence_scores)



    sum = 0;
    for sent in sentence_scores:
        sum += sentence_scores[sent]
    average = int(sum / len(sentence_scores))
    # print(average)
    summary = ""
    for sent in sentence_tokens:
        if (sent in sentence_scores) and (sentence_scores[sent] < (3.2 * average)):
            if (len(summary) < 1550):
                summary += " " + str(sent)

    # print(summary)

    return render_template('output.html', summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
