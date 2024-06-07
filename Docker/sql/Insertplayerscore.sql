LOAD DATA LOCAL INFILE '/home/airflow/data/score.csv' 
INTO TABLE lol.playerscore
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;