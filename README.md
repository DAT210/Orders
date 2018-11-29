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
  
If you are using docker toolbox, the frontend page should now be accessible at  
http://192.168.99.100:26300/testapi

the API can be bypassed with:  
http://192.168.99.100:26300/testSession


And if you are running the newer docker, it should be accessible at:  
http://127.0.0.1:26300/testapi

the API can be bypassed with:  
http://127.0.0.1:26300/testSession
  
Command to bash into the mysql server:  
docker exec -it mysql /bin/bash  

## Database backup and restoration commands:
 **Backup**  
docker exec CONTAINER /usr/bin/mysqldump -u root --password=root DATABASE > backup.sql

 **Restore**  
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE


## API

__GET: /orders/api/orderID/ID__

To get all info in a spesific order, send a get request to the specified docker url at the top with this appended: /orders/api/orderID/ID.
* This will return the following json:
```json
  		{
		  "OrderID": "",
		  "CustomerID": "",
		  "OrderTime": "",
		  "PaymentMethod": "",
		  "DeliveryMethod": "",
		  "Price": "",
		  "Payed": ""
		}
```

__GET: /orders/api/courses/OrderID__

To get all courses in an Order, send a get request to the specified docker url at the top with this appended: /orders/api/courses/OrderID.
* This will return the following json:
```json
  		[{
		  "OrderID": "",
		  "CourseID": "",
		  "CourseName": "",
		  "Quantity": "",
		  "Price": ""
		}]
```

__GET: /orders/api/customerorders/CustomerID__

If you want the order history of a customer send a get request to the specified docker url at the top with this appended: /orders/api/customerorders/CustomerID.

* This will return the following json:
```json
  		[{
		  "OrderID": "",
		  "CustomerID": "",
		  "OrderTime": "",
		  "PaymentMethod": "",
		  "DeliveryMethod": "",
		  "Price": "",
		  "Payed": ""
		}]
```
<!-- mysql -u <user> -p<password> <dbname> < file.sql -->
<!-- THIS MAY HAVE WORKED -->
