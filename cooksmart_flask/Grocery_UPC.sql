USE cooksmart;

DROP TABLE IF EXISTS GroceryUPC;
CREATE TABLE GroceryUPC
(
  id              int unsigned NOT NULL auto_increment, 
  upc14           VARCHAR(255) NOT NULL,                # Full title of the book
  upc12          VARCHAR(20) NOT NULL,                # The author of the book
  brand				VARCHAR(255),
  name				VARCHAR(255),
  PRIMARY KEY     (id)
);