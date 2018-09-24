Orders - Group 6
=======

**Getting Started:**
* Clone repository
* In cmd/terminal: cd into repository location
* Run: "docker-compose up --build"  
  
The container should now be running at http://192.168.99.100:4000/ 
  
mySQL port:3306  
  
Command to bash into the mysql server:
docker exec -it mysql /bin/bash  

## Database backup and restoration commands:
 **Backup**  
docker exec CONTAINER /usr/bin/mysqldump -u root --password=root DATABASE > backup.sql

 **Restore**  
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
