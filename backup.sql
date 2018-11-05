-- MySQL dump 10.13  Distrib 8.0.12, for Linux (x86_64)
--
-- Host: localhost    Database: Orders
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Orders` (
  `OrderID` int(11) NOT NULL AUTO_INCREMENT,
  `CustomerID` int(11) Default NULL,
  `OrderTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `PaymentMethod` varchar(12) Default NULL,
  `DeliveryMethod` varchar(12) Default NULL,
  `Price` float(11) NOT NULL,
  `Paid` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;


--
-- Table structure for table `Ingredients`
--

DROP TABLE IF EXISTS `Courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Courses` (
  `OrderID` int(11) NOT NULL,
  `CourseID` int(11) NOT NULL,
  `CourseName` varchar(32) NOT NULL,
  `Quantity` int(11) DEFAULT 0,
  `Price` float(11) DEFAULT 0,
  PRIMARY KEY (`CourseID`, `OrderID`),
  FOREIGN KEY(`OrderID`) REFERENCES `Orders`(`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ingredients`
--

LOCK TABLES `Courses` WRITE;
/*!40000 ALTER TABLE `Ingredients` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ingredients` ENABLE KEYS */;
UNLOCK TABLES;

INSERT INTO Orders(OrderID, CustomerID, PaymentMethod, DeliveryMethod, Price, Paid)
VALUES(1, 1, "Cash", "Car", "34.2", 1);

INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price)
VALUES(1, 1, "Margarita", 3, 5.20);

INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price)
VALUES(1, 2, "Pepperoni", 3, 6.35);

INSERT INTO Orders(OrderID, CustomerID, PaymentMethod, DeliveryMethod, Price, Paid)
VALUES(2, 15, "Credit", "Transit", "15.2", 1);

INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price)
VALUES(2, 8, "El Diabolo", 3, 7.20);

INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price)
VALUES(2, 6, "Pineapple", 3, 4.35);

INSERT INTO Orders(OrderID, CustomerID, PaymentMethod, DeliveryMethod, Price, Paid)
VALUES(3, 1, "Credit", "Pickup", "9.2", 1);

INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price)
VALUES(3, 2, "Pepperoni", 3, 6.35);

INSERT INTO Courses(OrderID, CourseID, CourseName, Quantity, Price)
VALUES(3, 6, "Pineapple", 3, 4.35);



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-03 13:20:23
