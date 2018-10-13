import spacy
import spacy.matcher
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')
nlp_sent = ""
sent = ""
openingTimesList = ['opening', 'open']
matcher = PhraseMatcher(nlp.vocab)

response = ""


def init():
    patterns = [nlp(text) for text in openingTimesList]
    matcher.add('openingTimes', None, *patterns)


def respond(sentence):
    prep_sentence(sentence)
    matches = get_match_id()
    for match in matches:
        sort(match)


def prep_sentence(sentence):
    global sent
    sent = sentence
    nlpsent = nlp(sent)
    global nlp_sent
    nlp_sent = nlpsent
    # lemma before saving as nlp_sent


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
        print('openingTimes')


def opening_times():
    print("")


def testing():
    tester = nlp(u"opening times Thursday")
    for ent in tester.ents:
        if ent.label_ == 'DATE':
            print("dato")


init()
respond("opening")
