from flask import json
import spacy
import sqlshit as sql
import fakereturn as fr

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

nlp = spacy.load('en_core_web_lg')
sent = ""
nlp_sent = ""


def not_handled():
    price_comp = nlp("What is the price")
    availability_comp = nlp("Is a table available")
    book_comp = nlp("I want to book a table")
    similarity = {
        'price': nlp_sent.similarity(price_comp),
        'availability': nlp_sent.similarity(availability_comp),
        'book': nlp_sent.similarity(book_comp)
    }
    most_likely = max(similarity, key=similarity.get)
    sql.notHandled(sent, most_likely, 0)
    return "You asked a question I couldn't even sort out. " \
           "I have been programmed to sort out any intelligent question a customer might have. " \
           "This means that your question is stupid, you're stupid, and your mom is stupid. <br/>"


def opening_times():
    date = False
    for entity in nlp_sent.ents:
        if entity.label_ == 'DATE':
            date = True
            if entity.text in weekdays:
                return sql.openingDay(entity.text)
            else:
                sql.notHandled(sent, "opening", 1)
                print(entity.text)
                return "I don't know the opening times on specific dates, too bad. </br>"
    if not date:
        return sql.allOpening()


def prices():
    # TODO find a way to sort out dish names
    sql.notHandled(sent, "price", 2)
    info = json.loads(fr.price('pepperoni pizza'))
    print(info)
    return "I can't answer questions about prices, " \
           "as anyone with half a brain could check it out for themselves IN THE MENU </br>"


def available():
    sql.notHandled(sent, "available", 3)
    for entity in nlp_sent.ents:
        print(entity.text)
        if entity.label_ == 'DATE':
            if entity.text in weekdays:
                print("weekday")
                # TODO make weekday into a specific data
    return "I can't answer questions about table availability, " \
           "as anyone with half a brain could check it out for themselves if they just followed THIS link </br>"


def complaint():
    sql.complaint(sent, 0)
    return "Your complaint has been saved, and will be reviewed whenever we feel like it (most likely never). " \
           "Thank you for not having a life (punk ass bitch). </br>"


def location():
    return "The address for the restaurant is ADDRESS, which you would have known if you'd looked here. </br>"


def joke():
    return "How do you stop a baby from crawling around in circles? Nail it’s other hand to the floor. </br>"
