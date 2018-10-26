import mysql.connector

configuration = {
    'user': 'root',
    'password': 'root',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'spacy',
    'raise_on_warnings': True,
}

conn = mysql.connector.connect(**configuration)
cur = conn.cursor()


def allOpening():
    sql = "SELECT * from openingTimes"
    cur.execute(sql)
    response = "We're usually open during these hours:<br/>"
    for row in cur:
        response += row[0] + ": " + row[1] + "-" + row[2] + "<br/>"
    return response


def openingDay(day):
    cur.execute("SELECT * from openingTimes WHERE weekday = '%s'" % day)
    for row in cur:
        response = "On " + row[0] + "s we're open from " + row[1] + " until " + row[2]
    return response
