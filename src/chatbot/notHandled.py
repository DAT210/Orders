import sqlshit as sql

notHandled = sql.getNotHandled()
for sent in notHandled:
    print("Sentence: " + sent[0])
    print("guess: " + sent[1])
