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
