SELECT Books.bookID as BookID, Books.title AS Title, Authors.authorName AS Author, Publishers.publisherName as Publisher, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity 
FROM Books 
INNER JOIN Authors ON Authors.authorID = Books.authorID 
INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID 
ORDER BY Books.title;