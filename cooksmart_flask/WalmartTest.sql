USE cooksmart;

DROP TABLE IF EXISTS Test;
CREATE TABLE Test
(
  id              int unsigned NOT NULL auto_increment, 
  product           VARCHAR(255) NOT NULL,    
  brand				VARCHAR(20),           
  amount         	VARCHAR(20) NOT NULL,                
  unit				VARCHAR(20),
  price				VARCHAR(10), #FLOAT(8,2),
  PRIMARY KEY     (id)
);