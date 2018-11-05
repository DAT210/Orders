![Logo of the project](/images/logo.png)


Orders - Group 6
=======

## Developing:

### Built with  
* Python 3.7 
* Mysql 8.0.12
* Docker 18.03.0

### Prerequisites
 * [Docker](https://www.docker.com/)
 * [GIT](https://git-scm.com/downloads)

## Getting Started:

### Setting up Dev  
* git clone https://github.com/DAT210/Orders.git
* In cmd/terminal: cd into repository location
* Run: docker-compose up --build  
  
If you are using docker toolbox, the container should now be visible at  
http://192.168.99.100:4000/  

And if you are running the newer docker, it should be visible at:  
http://127.0.0.1:4000/
  
Command to bash into the mysql server:  
docker exec -it mysql /bin/bash  

## Database backup and restoration commands:
 **Backup**  
docker exec CONTAINER /usr/bin/mysqldump -u root --password=root DATABASE > backup.sql

 **Restore**  
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE


## API
**IMPORTANT:** This is subject to change

* To get all courses in a given OrderID:
  * /orders/api/courses/"OrderID"
* To get all orders a customer have:
  * /orders/api/customerorders/"CustomerID"
<!-- mysql -u <user> -p<password> <dbname> < file.sql -->
<!-- THIS MAY HAVE WORKED -->
