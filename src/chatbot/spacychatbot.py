import spacy
import spacy.matcher
from flask import Flask, render_template, json, request
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import sqlshit as sql
import fakereturn as fr
import handler as h

nlp = spacy.load('en_core_web_lg')
nlp_sent = ""
sent = ""
openingTimesList = ['open', 'opening']
priceList = ['price', 'cost', 'how much']
availabilityList = ['available']
complaintsList = ['bad', 'horrible', 'terrible', 'dirty', 'slow']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
locationList = ['where', 'address']
jokeList = ['joke', 'funny']
recommendList = ['recommend']
matcher = PhraseMatcher(nlp.vocab)

app = Flask(__name__)

response = ""


@app.route("/")
def html():
    return render_template("tester.html")


@app.route("/init")
def init():
    opening_pattern = [nlp(text) for text in openingTimesList]
    price_pattern = [nlp(text) for text in priceList]
    available_pattern = [nlp(text) for text in availabilityList]
    complaints_pattern = [nlp(text) for text in complaintsList]
    location_pattern = [nlp(text) for text in locationList]
    joke_pattern = [nlp(text) for text in jokeList]
    rec_pattern = [nlp(text) for text in recommendList]
    matcher.add('openingTimes', None, *opening_pattern)
    matcher.add('prices', None, *price_pattern)
    matcher.add('availability', None, *available_pattern)
    matcher.add('complaints', None, *complaints_pattern)
    matcher.add('location', None, *location_pattern)
    matcher.add('joke', None, *joke_pattern)
    matcher.add('rec', None, *rec_pattern)
    return json.dumps("Hello")


@app.route("/respond")
def respond():
    global response
    response = ""
    sentence = request.args.get("sentence", None)
    prep_sentence(sentence)
    matches = get_matches()
    if not matches:
        response = h.not_handled()
    else:
        for match in matches:
            sort(match)
    return json.dumps(response)


def prep_sentence(sentence):
    # save sentence in case it isn't handled
    global sent
    sent = sentence
    h.sent = sent
    nlpsent = nlp(sent)
    # lemmatize to remove some word variations
    global nlp_sent
    nlp_sent = lemmatize(nlpsent)
    h.nlp_sent = nlp_sent


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
    global response
    match_id = match['id']
    rule_id = nlp.vocab.strings[match_id]
    if rule_id == "openingTimes":
        response = h.opening_times()
    elif rule_id == "prices":
        response = h.prices()
    elif rule_id == 'availability':
        response = h.available()
    elif rule_id == 'complaints':
        response = h.complaint()
    elif rule_id == 'location':
        response = h.location()
    elif rule_id == 'joke':
        response = h.joke()
    elif rule_id == 'rec':
        response = h.rec()
    else:
        response = h.not_handled()


if __name__ == "__main__":
    app.run()
