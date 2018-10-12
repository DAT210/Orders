import spacy
import spacy.matcher
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
nlp = spacy.load('en_core_web_sm')
sent = ""
openingTimesList = ['opening', 'open']
matcher = PhraseMatcher(nlp.vocab)


def init():
    patterns = [nlp(text) for text in openingTimesList]
    matcher.add('openingTimes', None, *patterns)
    testing()
    get_match_id("opening? times thursdays")


def get_match_id(sentence):
    global sent
    sent = sentence
    sentence = nlp(sentence)
    matches = matcher(sentence)
    for match_id, start, end in matches:
        sort(match_id, start, end)


def sort(id, start, end):
    print(id)
    if id == 1715934218517773148:
        print('openingTimes')


def opening_times():
    print("")


def testing():
    tester = nlp(u"opening times Thursday")
    for ent in tester.ents:
        if ent.label_ == 'DATE':
            print("dato")


init()
