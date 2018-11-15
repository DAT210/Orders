from textblob import TextBlob
from textblob import Word

text = "Opening"
low = text.lower()
w = Word(low)
lem = w.lemmatize()
print(lem)
