USE cooksmart;

DROP TABLE IF EXISTS cache;
CREATE TABLE cache
(
  id              int unsigned NOT NULL auto_increment, 
  product           VARCHAR(255) NOT NULL,              
  amount         	FLOAT(8,2) NOT NULL,                
  unit				VARCHAR(20) NOT NULL,
  price				VARCHAR(10) NOT NULL, 
  brand				VARCHAR(20),
  set_num			int,
  PRIMARY KEY     (id)
);