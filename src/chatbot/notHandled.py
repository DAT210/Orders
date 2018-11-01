import sqlshit as sql

notHandled = sql.getNotHandled()
for sent in notHandled:
    print(sent[0])
