from textblob import TextBlob

text = "What does the large pepperoni pizza cost?"
blob = TextBlob(text)
print(blob.tags)
print(blob.noun_phrases)
