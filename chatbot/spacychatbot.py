import mysql.connector
import spacy
import spacy.matcher
from flask import Flask, render_template
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')
nlp_sent = ""
sent = ""
openingTimesList = ['open', 'opening']
matcher = PhraseMatcher(nlp.vocab)

app = Flask(__name__)

response = ""


@app.route("/")
def html():
    return render_template("tester.html")


def init():
    patterns = [nlp(text) for text in openingTimesList]
    matcher.add('openingTimes', None, *patterns)
    print("init is running")


def send_response():
    # send response to js(?)
    pass


def send_question():
    # send question about whether their question was adequately answered??
    # wait for answer??
    pass


def respond(sentence):
    prep_sentence(sentence)
    matches = get_matches()
    if not matches:
        print("no match")
    else:
        for match in matches:
            sort(match)
        send_response()


def prep_sentence(sentence):
    # save sentence in case it isn't handled
    global sent
    sent = sentence
    nlpsent = nlp(sent)
    print(nlpsent)
    # lemmatize to remove plurals
    global nlp_sent
    nlp_sent = lemmatize(nlpsent)
    print(nlp_sent)


def lemmatize(nlpobj):
    lemma = ""
    for token in nlpobj:
        lemma += (token.lemma_ + " ")
    return nlp(lemma)


def get_matches():
    matches = matcher(nlp_sent)
    allmatches = []
    for match_id, start, end in matches:
        match = {
            'id': match_id,
            'start': start,
            'end': end
        }
        allmatches.append(match)
    return allmatches


def sort(match):
    print(match['id'])
    match_id = match['id']
    if match_id == 1715934218517773148:
        opening_times()
    else:
        not_handled()


def not_handled():
    print("I can't answer that question, sorry. ")


def opening_times():
    global response
    print("Handle opening times")
    response += "Your question about opening times cannot be answered yet."


if __name__ == "__main__":
    app.run()
