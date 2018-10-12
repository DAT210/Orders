import spacy

nlp = spacy.load('en_core_web_sm')
tester = nlp("what is the price")
text = nlp("what does the pepperoni pizza cost?")
q2 = nlp("how much is the vegetable platter?")
q1 = nlp("what is the price of the steak?")
print(tester.similarity(text))
print(tester.similarity(q2))
print(tester.similarity(q1))
