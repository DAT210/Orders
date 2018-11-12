from flask import json
import spacy
import sqlshit as sql
import fakereturn as fr
import random

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

nlp = spacy.load('en_core_web_lg')
sent = ""
nlp_sent = ""

jokes = ["How do you stop a baby from crawling around in circles? </br> Nail it’s other hand to the floor. </br>",
         "Which sexual position produces the ugliest children? </br> Ask your mother. </br>",
         "Your face </br>"]


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
    sql.notHandled(sent, most_likely, "no")
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
                sql.notHandled(sent, "opening", "yes")
                return "I don't know the opening times on specific dates, too bad. </br>"
    if not date:
        return sql.allOpening()


def prices():
    # TODO find a way to sort out dish names
    sql.notHandled(sent, "price", "yes")
    info = json.loads(fr.price('pepperoni pizza'))
    return "I can't answer questions about prices, " \
           "as anyone with half a brain could check it out for themselves IN THE MENU </br>"


def available():
    sql.notHandled(sent, "available", "yes")
    date = False
    for entity in nlp_sent.ents:
        if entity.label_ == 'DATE':
            date = True
            if entity.text in weekdays:
                # TODO make weekday into a specific date
                print("placeholder")
    if not date:
        # TODO find today's date ?
        print("Why is there no date??")
    return "I can't answer questions about table availability, " \
           "as anyone with half a brain could check it out for themselves if they just followed THIS link </br>"


def complaint():
    # TODO should the complaints be sent somewhere on the employee website?
    sql.complaint(sent, 0)
    return "Your complaint has been saved, and will be reviewed whenever we feel like it (most likely never). " \
           "Thank you for not having a life (punk ass bitch). </br>"


def location():
    return "The address for the restaurant is ADDRESS, which you would have known if you'd looked here. </br>"


def joke():
    my_joke = random.choice(jokes)
    return my_joke


def rec():
    return "I don't know you well enough to recommend food for you. " \
           "Why don't we go on a few dates so that I can eventually get tired of you, " \
           "cheat on you and then leave you for someone younger and prettier? </br>"
