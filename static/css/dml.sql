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
UPDATE Books 
SET Books.bookID = :bookIDInput, Books.title = :titleInput, Books.authorID = (SELECT authorID FROM Authors WHERE :authorInput = Authors.authorName),
	Books.publisherID = (SELECT publisherID FROM Publishers WHERE :publisherInput = Publishers.publisherName),
    Books.genre = :genreInput, Books.price = :priceInput, Books.inventoryQty = :inventoryQtyInput;
    







-- Purchases table CRUD operations
SELECT Purchases.purchaseID, Customers.customerName as Customer, Purchases.datePlaced, Purchases.purchaseStatus
	FROM Customers
    INNER JOIN Purchases ON Customers.customerID = Purchases.customerID;

INSERT INTO Purchases (datePlaced, customerID, purchaseStatus)
VALUES (:datePlacedInput, (SELECT customerID from Customers WHERE customerName = :inputName), :purchaseStatusInput);

--Move BookPurchases INSERT query here?


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

