LOAD DATA LOCAL INFILE '/home/airflow/data/match.csv' 
INTO TABLE lol.match
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;