import spacy
import spacy.matcher
from flask import Flask, render_template, json, request
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import sqlshit as sql
import fakereturn as fr

nlp = spacy.load('en_core_web_lg')
nlp_sent = ""
sent = ""
openingTimesList = ['open', 'opening']
priceList = ['price', 'cost', 'how much']
availabilityList = ['available']
complaintsList = ['bad', 'horrible', 'terrible', 'dirty', 'slow']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
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
    matcher.add('openingTimes', None, *opening_pattern)
    matcher.add('prices', None, *price_pattern)
    matcher.add('availability', None, *available_pattern)
    matcher.add('complaints', None, *complaints_pattern)
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
    elif rule_id == "prices":
        prices()
    elif rule_id == 'availability':
        available()
    elif rule_id == 'complaints':
        complaint()
    else:
        not_handled()


def not_handled():
    global response
    price_comp = nlp("What is the price")
    availability_comp = nlp("Is a table available")
    book_comp = nlp("I want to book a table")
    similarity = {
        'price': nlp_sent.similarity(price_comp),
        'availability': nlp_sent.similarity(availability_comp),
        'book': nlp_sent.similarity(book_comp)
    }
    mostLikely = max(similarity, key=similarity.get)
    sql.notHandled(sent, mostLikely)
    response += "I can't answer that question, sorry. <br/>"


def opening_times():
    date = False
    global response
    for entity in nlp_sent.ents:
        if entity.label_ == 'DATE':
            print(entity.text)
            date = True
            if entity.text in weekdays:
                response += sql.openingDay(entity.text)
            else:
                response += "I don't know the opening times on specific dates, sorry. </br>"
    if not date:
        response = sql.allOpening()


def prices():
    global response
    response += "I don't know the prices of specific dishes yet, " \
                "but you could visit THE MENU and see for yourself </br>"
    myjson = fr.price('pepperoni pizza')
    info = json.loads(myjson)
    print(info['Price'])


def available():
    global response
    response += "I can't answer questions about table availability yet, " \
                "but you are welcome to check it out for yourself. </br>"


def complaint():
    global response
    response = "Your complaint has been saved, and will be reviewed whenever we feel like it (most likely never). " \
               "Thank you for not having anything else to do. </br>"


if __name__ == "__main__":
    app.run()
