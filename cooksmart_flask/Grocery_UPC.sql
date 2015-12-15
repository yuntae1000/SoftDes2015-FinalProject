USE cooksmart;

DROP TABLE IF EXISTS GroceryUPC;
CREATE TABLE GroceryUPC
(
  id              int unsigned NOT NULL auto_increment, 
  product           VARCHAR(255) NOT NULL,                # Full title of the book
  amount          VARCHAR(20) NOT NULL,                # The author of the book
  brand				VARCHAR(255),
  name				VARCHAR(255),
  PRIMARY KEY     (id)
);