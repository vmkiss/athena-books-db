-- Group 25 Data Manipulation Queries
-- : used to denote values that will contain variables readable by NodeJS

-- Publishers table CRUD operations
INSERT INTO Publishers (publisherName, publisherAddress, publisherCity, publisherState, publisherZip)
VALUES (:publisherNameInput, :publisherAddressInput, :publisherCityInput, :publisherStateInput, :publisherZipInput);

SELECT publisherID, AS PublisherID publisherName AS Name, publisherAddress AS Address, publisherCity AS City, publisherState AS State, publisherZip AS ZipCode
FROM Publishers;

-- Authors table CRUD operations
INSERT INTO Authors (authorName, publisherID)
VALUES (:authorInput, :publisherInput));

SELECT Authors.authorID AS AuthorID, Authors.authorName AS Name, Publishers.publisherName as Publisher
    FROM Authors
    INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID;

--Populate publisher dropdown form
SELECT publisherID, publishername 
FROM Publishers 
ORDER BY publisherName;

-- Customers table CRUD operations
INSERT INTO Customers (customerName, customerPhone, customerEmail, customerAddress, customerCity, customerState, customerZip)
VALUES (:customerNameInput, :customerPhoneInput, :customerEmailInput, :customerAddressInput, :customerCityInput, :customerStateInput, :customerZipInput);

SELECT customerID AS CustomerID, customerName AS Name, customerPhone AS Phone, customerEmail AS Email, customerAddress AS Address, customerCity AS City, customerState AS State, customerZip AS ZipCode
    FROM Customers;

UPDATE Customers
SET customerName = :customerNameInput, customerPhone = :customerPhoneInput, customerEmail = :customerEmailInput, customerAddress = :customerAddressInput,
customerCity = :customerCityInput, customerState = :customerStateInput, customerZip = :customerZipInput
WHERE customerID = :customerIDInput;

-- Books table CRUD operations
INSERT INTO Books (title, authorID, publisherID, genre, price, inventoryQty)
VALUES (:titleInput, :authorInput, 
	   (SELECT publisherID FROM Authors WHERE authorID=:authorInput), 
       :genreInput, :priceInput, :inventoryQtyInput);

SELECT Books.bookID as BookID, Books.title AS Title, Authors.authorName AS Author, Publishers.publisherName as Publisher, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity 
FROM Books 
INNER JOIN Authors ON Authors.authorID = Books.authorID 
INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID 
ORDER BY Books.title;

--Populate Author dropdown form
SELECT authorID, authorName FROM Authors;

DELETE FROM Books WHERE bookID = :bookIDInput;

--Edit Book details

--Diplay current info of book to be edited
SELECT Books.bookID as BookID, Publishers.publisherName as Publisher, Authors.authorName AS Author, Books.title AS Title, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity 
FROM Books 
INNER JOIN Authors ON Authors.authorID = Books.authorID 
INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID WHERE BookID = :bookIDInput;

--Populate Author dropdown form
SELECT authorID, authorName FROM Authors;

UPDATE Books 
SET Books.title = :titleInput, Books.authorID = :authorInput, Books.genre = :genreInput, Books.price = priceInput, Books.inventoryQty = inventoryQtyInput
WHERE BookID = :bookIDInput;
    
-- Purchases table CRUD operations

--Insert Purchase without Customer
INSERT INTO Purchases (customerID, datePlaced, purchaseStatus) 
VALUES (NULL, :datePlacedInput, :purchaseStatusInput);

--Insert Purchase with Customer
INSERT INTO Purchases (customerID, datePlaced, purchaseStatus) 
VALUES (:customerIDInput, :datePlacedInput, purchaseStatusInput);

--View purchases
SELECT Purchases.purchaseID AS PurchaseID, Customers.customerName AS Customer, Purchases.datePlaced AS Date, Purchases.purchaseStatus AS STATUS
	FROM Purchases
    LEFT JOIN Customers ON Customers.customerID = Purchases.customerID;

--Populate Book dropdown form
SELECT bookID, title FROM Books;

--Populate Customer dropdown form
SELECT customerID, customerName FROM Customers

--Delete Purchase
DELETE FROM Purchases WHERE PurchaseID = :purchaseIDInput;

--Edit Purchase details

--Diplay details of current Purchase
SELECT Purchases.purchaseID AS PurchaseID, Customers.customerName AS Customer, Purchases.datePlaced AS Date, Purchases.purchaseStatus AS Status 
FROM Purchases 
LEFT JOIN Customers ON Customers.customerID = Purchases.customerID WHERE PurchaseID = purchaseIDInput;

--Populate Customer dropdown form
SELECT customerID, customerName FROM Customers;

--Edit Purchase without Customer
UPDATE Purchases SET customerID=NULL, Purchases.datePlaced=:datePlacedInput, Purchases.purchaseStatus=purchaseStatusInput WHERE PurchaseID=:purchaseIDInput;

--Edit Purchase with Customer
UPDATE Purchases SET Purchases.customerID=customerIDInput, Purchases.datePlaced=:datePlacedInput, Purchases.purchaseStatus=:purchaseStatusInput WHERE PurchaseID=:purchaseIDInput;




--Remove ability to update purchaseID?  
UPDATE Purchases
SET Purchases.purchaseID = :purchaseIDInput, Purchases.datePlaced = :datePlacedInput, Purchases.purchaseStatus = purchaseStatusInput;
    
DELETE FROM Purchases WHERE purchaseID = :purchaseIDInput;

    
-- BookPurchases (intersection) table CRUD operations
SELECT BookPurchases.bookPurchasesID, Books.title as Book, Purchases.purchaseID as PurchaseID, 
BookPurchases.invoiceDate, BookPurchases.orderQty, BookPurchases.unitPrice, BookPurchases.lineTotal
	FROM BookPurchases
    INNER JOIN Books ON Books.bookID = BookPurchases.bookID
    INNER JOIN Purchases ON BookPurchases.purchaseID = Purchases.purchaseID;

--INSERT INTO BookPurchases (bookPurchasesID, invoiceDate, orderQty, unitPrice, lineTotal)
--VALUES (:bookPurchaseIDInput, :invoiceDateInput; :orderQtyInput, :unitPriceInput, :lineTotalInput);

<!-- using user input from Purchases form-->
INSERT INTO BookPurchases (bookID, purchaseID, invoiceDate, orderQty, unitPrice, lineTotal) 
VALUES ((SELECT bookID FROM Books WHERE Books.title = :bookTitleInput), 
(SELECT purchaseID FROM Purchases WHERE Purchases.customerID = (SELECT customerID FROM Customers WHERE Customers.customerName = :userInputName) AND Purchases.datePlaced = :invoiceDateInput), 
:invoiceDateInput, :orderQtyInput, (SELECT price FROM Books WHERE Books.title = :bookTitleInput), (orderQty * unitPrice));


--Remove ability to update bookPurchasesID? Do we really want the ability to directly input unitPrice and lineTotal
UPDATE BookPurchases
SET BookPurchases.bookPurchasesID = :bookPurchaseInputID, BookPurchases.invoiceDate = :invoiceDateInput,
BookPurchases.orderQty = :orderQtyInput, BookPurchases.unitPrice = :unitPriceInput, BookPurchases.lineTotal = :lineTotalInput;

DELETE FROM BookPurchases WHERE Book_purchaseID = :bookPurchaseIDInput;


