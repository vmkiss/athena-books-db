-- MariaDB dump 10.19  Distrib 10.5.22-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_itochr
-- ------------------------------------------------------
-- Server version	10.6.16-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Authors`
--

DROP TABLE IF EXISTS `Authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Authors` (
  `authorID` int(11) NOT NULL AUTO_INCREMENT,
  `authorName` varchar(255) NOT NULL,
  `publisherID` int(11) NOT NULL,
  PRIMARY KEY (`authorID`),
  KEY `publisherID` (`publisherID`),
  CONSTRAINT `Authors_ibfk_1` FOREIGN KEY (`publisherID`) REFERENCES `Publishers` (`publisherID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Authors`
--

LOCK TABLES `Authors` WRITE;
/*!40000 ALTER TABLE `Authors` DISABLE KEYS */;
INSERT INTO `Authors` VALUES (1,'Harper Lee',1),(2,'P.G. Wodehouse',2),(3,'Terry Pratchett',3),(4,'Louisa May Alcott',3);
/*!40000 ALTER TABLE `Authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book_purchases`
--

DROP TABLE IF EXISTS `Book_purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Book_purchases` (
  `bookPurchasesID` int(11) NOT NULL AUTO_INCREMENT,
  `bookID` int(11) NOT NULL,
  `purchaseID` int(11) NOT NULL,
  `invoiceDate` date NOT NULL,
  `orderQty` int(11) NOT NULL,
  `unitPrice` decimal(19,2) NOT NULL,
  `lineTotal` decimal(19,2) NOT NULL,
  PRIMARY KEY (`bookPurchasesID`),
  KEY `bookID` (`bookID`),
  KEY `purchaseID` (`purchaseID`),
  CONSTRAINT `Book_purchases_ibfk_1` FOREIGN KEY (`bookID`) REFERENCES `Books` (`bookID`) ON UPDATE CASCADE,
  CONSTRAINT `Book_purchases_ibfk_2` FOREIGN KEY (`purchaseID`) REFERENCES `Purchases` (`purchaseID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book_purchases`
--

LOCK TABLES `Book_purchases` WRITE;
/*!40000 ALTER TABLE `Book_purchases` DISABLE KEYS */;
INSERT INTO `Book_purchases` VALUES (1,3,1,'2024-01-05',1,15.98,15.98),(2,1,2,'2024-02-01',1,16.99,16.99),(3,4,3,'2024-01-30',2,17.99,35.98),(4,4,4,'2024-02-06',1,17.99,17.99),(5,2,4,'2024-02-06',1,19.99,19.99);
/*!40000 ALTER TABLE `Book_purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Books` (
  `bookID` int(11) NOT NULL AUTO_INCREMENT,
  `publisherID` int(11) NOT NULL,
  `authorID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `price` decimal(19,2) DEFAULT NULL,
  `inventoryQty` int(3) DEFAULT NULL,
  PRIMARY KEY (`bookID`),
  KEY `publisherID` (`publisherID`),
  KEY `authorID` (`authorID`),
  CONSTRAINT `Books_ibfk_1` FOREIGN KEY (`publisherID`) REFERENCES `Publishers` (`publisherID`) ON UPDATE CASCADE,
  CONSTRAINT `Books_ibfk_2` FOREIGN KEY (`authorID`) REFERENCES `Authors` (`authorID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Books`
--

LOCK TABLES `Books` WRITE;
/*!40000 ALTER TABLE `Books` DISABLE KEYS */;
INSERT INTO `Books` VALUES (1,1,1,'To Kill a Mockingbird','literary',16.99,105),(2,2,2,'Right Ho, Jeeves','humor',19.99,14),(3,3,3,'Monstrous Regiment','fantasy',15.98,25),(4,3,4,'Little Women','literary',17.99,36);
/*!40000 ALTER TABLE `Books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customers` (
  `customerID` int(11) NOT NULL AUTO_INCREMENT,
  `customerName` varchar(255) NOT NULL,
  `customerPhone` varchar(10) DEFAULT NULL,
  `customerEmail` varchar(255) NOT NULL,
  `customerAddress` varchar(255) NOT NULL,
  `customerCity` varchar(255) NOT NULL,
  `customerState` varchar(2) NOT NULL,
  `customerZip` varchar(5) NOT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customers`
--

LOCK TABLES `Customers` WRITE;
/*!40000 ALTER TABLE `Customers` DISABLE KEYS */;
INSERT INTO `Customers` VALUES (1,'Daisy Jones',NULL,'djones@gmail.com','12345 SE 12th Ave','Portland','OR','97221'),(2,'Madeline Smith','6501239876','maddie123@gmail.com','1972 Iliff Ave','Denver','CO','80110'),(3,'Archibald Eggleton','5033104395','asmith@gmail.com','473 Seneca Drive','Portland','OR','97205'),(4,'Ophelia Bloom','3609702377','bloomo@hotmail.com','2376 Pratt Avenue','Olympia','WA','98501');
/*!40000 ALTER TABLE `Customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Publishers`
--

DROP TABLE IF EXISTS `Publishers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Publishers` (
  `publisherID` int(11) NOT NULL AUTO_INCREMENT,
  `publisherName` varchar(255) NOT NULL,
  `publisherAddress` varchar(255) NOT NULL,
  `publisherCity` varchar(255) NOT NULL,
  `publisherState` varchar(2) NOT NULL,
  `publisherZip` varchar(5) NOT NULL,
  PRIMARY KEY (`publisherID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Publishers`
--

LOCK TABLES `Publishers` WRITE;
/*!40000 ALTER TABLE `Publishers` DISABLE KEYS */;
INSERT INTO `Publishers` VALUES (1,'HarperCollins','195 Broadway','New York','NY','10007'),(2,'Simon & Schuster','1230 Avenue of the Americas','New York','NY','10020'),(3,'Penguin Random House','1745 Broadway','New York','NY','10019');
/*!40000 ALTER TABLE `Publishers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchases`
--

DROP TABLE IF EXISTS `Purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Purchases` (
  `purchaseID` int(11) NOT NULL AUTO_INCREMENT,
  `customerID` int(11) NOT NULL,
  `datePlaced` date NOT NULL,
  `totalPrice` decimal(19,2) DEFAULT NULL,
  `purchaseStatus` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`purchaseID`),
  KEY `customerID` (`customerID`),
  CONSTRAINT `Purchases_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `Customers` (`customerID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchases`
--

LOCK TABLES `Purchases` WRITE;
/*!40000 ALTER TABLE `Purchases` DISABLE KEYS */;
INSERT INTO `Purchases` VALUES (1,1,'2024-01-05',15.98,'Complete'),(2,2,'2024-02-01',16.99,'Shipped'),(3,3,'2024-01-30',35.98,'Shipped'),(4,4,'2024-02-06',37.98,'Processing');
/*!40000 ALTER TABLE `Purchases` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-28  9:01:39
