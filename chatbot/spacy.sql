CREATE DATABASE spacy;
USE spacy;
CREATE TABLE unimplemented(sentence TEXT, id smallint unsigned not null auto_increment, constraint pk_example primary key (id))
CREATE TABLE openingTimes(weekday varchar(10), openingTime varchar(10), closingTime varchar(10))
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('monday', '12:00', '20:00')
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('tuesday', '12:00', '20:00')
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('wednesday', '12:00', '20:00')
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('thursday', '12:00', '20:00')
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('friday', '12:00', '20:00')
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('saturday', '12:00', '20:00')
INSERT INTO openingTimes(weekday, openingTime, closingTime) VALUES ('sunday', '12:00', '20:00')