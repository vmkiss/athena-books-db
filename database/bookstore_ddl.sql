-- Group 25: Christine Ito, Veronika Kiss

-- Citation: Code to set foreign key checks and disable commits 
-- Copied from CS 340 Canvas Assignment Project Step 2 Draft 
--URL: https://canvas.oregonstate.edu/courses/1946034/assignments/9456214
-- Date: 02/6/2024
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;


-- create Customer table
DROP TABLE IF EXISTS Customers;
CREATE TABLE Customers (
customerID INT(11) NOT NULL AUTO_INCREMENT, 
customerName VARCHAR(255) NOT NULL,
customerPhone VARCHAR(12) NOT NULL, 
customerEmail VARCHAR(255) NOT NULL,
customerAddress VARCHAR (255) NOT NULL, 
customerCity VARCHAR(255) NOT NULL,
customerState VARCHAR(2) NOT NULL,
customerZip VARCHAR(5) NOT NULL,
PRIMARY KEY (customerID)
);

-- create Publishers table
DROP TABLE IF EXISTS Publishers;
CREATE TABLE Publishers (
publisherID INT(11) NOT NULL AUTO_INCREMENT,
publisherName VARCHAR(255) NOT NULL, 
publisherAddress VARCHAR(255) NOT NULL, 
publisherCity VARCHAR(255) NOT NULL,
publisherState VARCHAR(2) NOT NULL,
publisherZip VARCHAR(5) NOT NULL,
PRIMARY KEY (publisherID)
);

-- create Authors table
DROP TABLE IF EXISTS Authors;
CREATE TABLE Authors (
authorID INT(11) NOT NULL AUTO_INCREMENT, 
authorName VARCHAR(255) NOT NULL, 
publisherID INT(11) NOT NULL,
PRIMARY KEY (authorID),
FOREIGN KEY (publisherID) REFERENCES Publishers(publisherID)
	ON UPDATE CASCADE
);


-- create Books table
DROP TABLE IF EXISTS Books;
CREATE TABLE `Books` (
bookID INT(11) NOT NULL AUTO_INCREMENT,
authorID INT(11) NOT NULL, 
title VARCHAR(255) NOT NULL, 
genre VARCHAR(255) NOT NULL,
price DECIMAL (19, 2) NOT NULL, 
inventoryQty INT(3) NOT NULL,
PRIMARY KEY (bookID),
FOREIGN KEY (authorID) REFERENCES Authors(authorID)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

-- create Purchases table
DROP TABLE IF EXISTS Purchases;
CREATE TABLE Purchases (
`purchaseID` INT(11) NOT NULL AUTO_INCREMENT, 
`customerID` INT(11) DEFAULT NULL, 
`datePlaced` DATE NOT NULL, 
`purchaseStatus` VARCHAR(255) NOT NULL,
PRIMARY KEY (`purchaseID`),
FOREIGN KEY (`customerID`) REFERENCES Customers(`customerID`) ON DELETE SET NULL ON UPDATE CASCADE
);

-- create BookPurchases table
-- intersection table between Books and Purchases
DROP TABLE IF EXISTS BookPurchases;
CREATE TABLE BookPurchases (
bookPurchasesID INT(11) NOT NULL AUTO_INCREMENT, 
bookID INT(11) NOT NULL, 
purchaseID INT(11) NOT NULL,  
orderQty INT(11) NOT NULL, 
unitPrice DECIMAL(19, 2) NOT NULL,
lineTotal DECIMAL (19, 2) NOT NULL,
PRIMARY KEY (bookPurchasesID),
FOREIGN KEY (bookID) REFERENCES Books(bookID)
	ON UPDATE CASCADE
	ON DELETE CASCADE, 
FOREIGN KEY (purchaseID) REFERENCES Purchases(purchaseID)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

-- inserts sample data into Customers table
INSERT INTO Customers (customerName, customerPhone, customerEmail, customerAddress, customerCity, customerState, customerZip)
VALUES ('Daisy Jones', '123-456-7890', 'djones@gmail.com', '12345 SE 12th Ave', 'Portland', 'OR', '97221'), 
('Madeline Smith', '650-123-9876', 'maddie123@gmail.com', '1972 Iliff Ave', 'Denver', 'CO', '80110'),
('Archibald Eggleton', '503-310-4395', 'asmith@gmail.com', '473 Seneca Drive', 'Portland', 'OR', '97205'),
('Ophelia Bloom', '360-970-2377', 'bloomo@hotmail.com', '2376 Pratt Avenue', 'Olympia', 'WA', '98501')
;

-- inserts sample data into Publishers table
INSERT INTO Publishers (publisherName, publisherAddress, publisherCity, publisherState, publisherZip)
VALUES ('HarperCollins', '195 Broadway', 'New York', 'NY', '10007'),
('Simon & Schuster', '1230 Avenue of the Americas', 'New York', 'NY', '10020'),
('Penguin Random House', '1745 Broadway', 'New York', 'NY', '10019')
;

-- inserts sample data into Authors table
INSERT INTO Authors (authorName, publisherID)
VALUES ('Harper Lee', (SELECT publisherID from Publishers WHERE publisherName = 'HarperCollins')),
('P.G. Wodehouse', (SELECT publisherID from Publishers WHERE publisherName = 'Simon & Schuster')),
('Terry Pratchett', (SELECT publisherID from Publishers WHERE publisherName = 'Penguin Random House')),
('Louisa May Alcott', (SELECT publisherID from Publishers WHERE publisherName = 'Penguin Random House'))
;

-- inserts sample data into Books table
INSERT INTO Books (authorID, title, genre, price, inventoryQty)
VALUES ((SELECT authorID FROM Authors WHERE authorName = 'Harper Lee'), 'To Kill a Mockingbird', 'Literary', 16.99, 105),
((SELECT authorID FROM Authors WHERE authorName = 'P.G. Wodehouse'), 'Right Ho, Jeeves', 'Humor', 19.99, 14),
((SELECT authorID FROM Authors WHERE authorName = 'Terry Pratchett'), 'Monstrous Regiment', 'Fantasy', 15.98, 25),
((SELECT authorID FROM Authors WHERE authorName = 'Louisa May Alcott'), 'Little Women', 'Literary', 17.99, 36)
;

-- inserts sample data into Purchases table
INSERT INTO Purchases (customerID, datePlaced, purchaseStatus)
VALUES ((SELECT customerID FROM Customers WHERE customerName = "Daisy Jones"), '2024-01-05', 'Complete'), 
((SELECT customerID FROM Customers WHERE customerName = "Madeline Smith"), '2024-02-01', 'Shipped'),
((SELECT customerID FROM Customers WHERE customerName = "Archibald Eggleton"), '2024-01-30', 'Shipped'),
((SELECT customerID FROM Customers WHERE customerName = "Ophelia Bloom"), '2024-02-06', 'Processing')
;

-- inserts sample data into BookPurchases table
INSERT INTO BookPurchases (bookID, purchaseID, orderQty, unitPrice, lineTotal)
VALUES ((SELECT bookID FROM Books WHERE title = 'Monstrous Regiment'), (SELECT purchaseID FROM Purchases WHERE customerID = (SELECT customerID from Customers WHERE customerName = 'Daisy Jones') AND datePlaced = '2024-01-05'), 1, (SELECT price FROM Books WHERE title = 'Monstrous Regiment' AND authorID = (SELECT authorID FROM Authors WHERE authorName = 'Terry Pratchett')), (orderQty * unitPrice)),
((SELECT bookID FROM Books WHERE title = 'To Kill a Mockingbird'), (SELECT purchaseID FROM Purchases WHERE customerID = (SELECT customerID from Customers WHERE customerName = 'Madeline Smith') AND datePlaced = '2024-02-01'), 1, (SELECT price FROM Books WHERE title = 'To Kill a Mockingbird' AND authorID = (SELECT authorID FROM Authors WHERE authorName = 'Harper Lee')), (orderQty * unitPrice)),
((SELECT bookID FROM Books WHERE title = 'Little Women'), (SELECT purchaseID FROM Purchases WHERE customerID = (SELECT customerID FROM Customers WHERE customerName = 'Archibald Eggleton') AND datePlaced = '2024-01-30'), 2, (SELECT price FROM Books WHERE title = 'Little Women' AND authorID = (SELECT authorID FROM Authors WHERE authorName = 'Louisa May Alcott')), (orderQty * unitPrice)),
((SELECT bookID FROM Books WHERE title = 'Little Women'), (SELECT purchaseID FROM Purchases WHERE customerID = (SELECT customerID FROM Customers WHERE customerName = 'Ophelia Bloom') AND datePlaced = '2024-02-06'), 1, (SELECT price FROM Books WHERE title = 'Little Women' AND authorID = (SELECT authorID FROM Authors WHERE authorName = 'Louisa May Alcott')), (orderQty * unitPrice)),
((SELECT bookID FROM Books WHERE title = 'Right Ho, Jeeves'), (SELECT purchaseID FROM Purchases WHERE customerID = (SELECT customerID FROM Customers WHERE customerName = 'Ophelia Bloom') AND datePlaced = '2024-02-06'), 1, (SELECT price FROM Books WHERE title = 'Right Ho, Jeeves' AND authorID = (SELECT authorID FROM Authors WHERE authorName = 'P.G. Wodehouse')), (orderQty * unitPrice))
;

-- Citation: code to enable commits and foreign key checks
-- Copied from CS 340 Canvas Assignment Project Step 2 Draft (https://canvas.oregonstate.edu/courses/1946034/assignments/9456214)
-- Date: 2/5/24

SET FOREIGN_KEY_CHECKS=1;
COMMIT;

