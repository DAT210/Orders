import spacy
import spacy.matcher
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')
nlp_sent = ""
sent = ""
openingTimesList = ['open', 'opening']
matcher = PhraseMatcher(nlp.vocab)

response = ""


def init():
    patterns = [nlp(text) for text in openingTimesList]
    matcher.add('openingTimes', None, *patterns)


def send_response():
    # send response to js(?)
    pass


def send_question():
    # send question about whether their question was adequately answered??
    # wait for answer??
    pass


def respond(sentence):
    prep_sentence(sentence)
    matches = get_match_id()
    for match in matches:
        sort(match)
    send_response()


def prep_sentence(sentence):
    global sent
    sent = sentence
    nlpsent = nlp(sent)
    # lemma before saving as nlp_sent
    global nlp_sent
    nlp_sent = lemmatize(nlpsent)
    print(nlpsent)
    print(nlp_sent)


def lemmatize(nlpobj):
    lemma = ""
    for token in nlpobj:
        lemma += (token.lemma_ + " ")
    return nlp(lemma)


def get_match_id():
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
    if match['id'] == 1715934218517773148:
        opening_times()


def opening_times():
    global response
    print("Handle opening times")
    response += "Your question about opening times cannot be answered yet."


def testing():
    tester = nlp(u"opening times Thursday")
    for ent in tester.ents:
        if ent.label_ == 'DATE':
            print("dato")


init()
respond("opening, open opens times Times time apples apple")
