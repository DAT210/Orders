import mysql.connector
import spacy
import spacy.matcher
from flask import Flask, render_template, json, request
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


@app.route("/init")
def init():
    patterns = [nlp(text) for text in openingTimesList]
    matcher.add('openingTimes', None, *patterns)
    return json.dumps("Hello")


@app.route("/respond")
def respond():
    global response
    response = ""
    sentence = request.args.get("sentence", None)
    prep_sentence(sentence)
    matches = get_matches()
    if not matches:
        not_handled()
    else:
        for match in matches:
            sort(match)
    return json.dumps(response)


def prep_sentence(sentence):
    # save sentence in case it isn't handled
    global sent
    sent = sentence
    nlpsent = nlp(sent)
    print(nlpsent)
    # lemmatize to remove some word variations
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
    rule_id = nlp.vocab.strings[match_id]
    print(rule_id)
    if rule_id == "openingTimes":
        opening_times()
    else:
        not_handled()


def not_handled():
    global response
    print("I can't answer that question, sorry. ")
    response += "I can't answer that question, sorry. "


def opening_times():
    global response
    print("Handle opening times")
    response += "Your question about opening times cannot be answered yet. "


def test(sentence):
    prep_sentence(sentence)
    matches = get_matches()
    if not matches:
        print("no match")
    else:
        for match in matches:
            sort(match)


if __name__ == "__main__":
    app.run()
