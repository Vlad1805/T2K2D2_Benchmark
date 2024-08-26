# Setup

This projects uses docker for running the database, sql and csv files for creating tables and inserting data, and python scripts for automating this proccesses.

First go to the scripts directory:
```
cd scripts
```
Create a virtual environmet in python:
```
python -m venv venv
```
Activate the virtual environment:
```
.\venv\Scripts\activate
```
Install dependencies:
```
pip install -r requirements.txt
```

# Running the benchmarks

First download the data set and save it in a directory named SetDate inside the scripts directory.

## Select the experiment

```
cd t2k2
```
or
```
cd t2k2d2
```
## The project structure for t2k2 and t2k2d2 should be:
```
├── create-tables.py
├── csv
│   ├── 1000K
│   ├── 1500K
│   ├── 2000K
│   ├── 2500K
│   ├── 500K
│   └── test
├── docker-compose-distributed.yml
├── docker-compose.yml
├── generate_csv.py
├── insert-data.py
├── logs
├── run-query.py
└── tables.sql
```

## First create the databse using docker

Single instance:
```
docker compose up -d
```

Distributed instance:
```
docker-compose -f docker-compose-distributed.yml down -d
```

## Create the tables

```
python create-tables.py
```

## Insert data

As the data files are rather big we will use batch inserts to fulfill this task in a optimal time using csv files.

### First lets generate the csv files using the generate_csv.py script:

```
python generate_csv.py --json_file=documents_clean500K
```

```
(venv) vstanciu@Vlads-MacBook-Pro-4 t2k2 % python generate_csv.py -h
usage: generate_csv.py [-h]
                       [--json_file {documents_clean500K.json,documents_clean1000K.json,documents_clean1500K.json,documents_clean2000K.json,documents_clean2500K.json,test.json}]
```

### The generated output can be found in the csv directory.
```
csv
├── 1000K
│   ├── authors.csv
│   ├── documents.csv
│   ├── documents_authors.csv
│   ├── genders.csv
│   ├── geo_location.csv
│   ├── vocabulary.csv
│   └── words.csv
├── 1500K
├── 2000K
├── 2500K
├── 500K
└── test
```

### Now we can insert the data using the insert-data.py script.

```
python insert-data.py --json_file=documents_clean500K.json
```

```
(venv) vstanciu@Vlads-MacBook-Pro-4 t2k2d2 % python insert-data.py -h
usage: insert-data.py [-h]
                      [--json_file {documents_clean500K.json,documents_clean1000K.json,documents_clean1500K.json,documents_clean2000K.json,documents_clean2500K.json,test.json}]
```

## Run a single query

Check the dictionary defined in run-query.py. The script will wait for you to enter a key. 

```
(venv) vstanciu@Vlads-MacBook-Pro-4 t2k2d2 % python run-query.py
Enter the ID of the SQL script to execute: 
```

## Generate time data

```
python generate-time-data.py
```

### You should see the output in logs/

```
logs
├── TopK_Documents
│   ├── OLAP_NuoDB_Okapi
│   │   ├── Q1_1w_female.sql.log
│   │   ├── Q1_1w_male.sql.log
│   │   ├── Q1_2w_female.sql.log
│   │   ├── Q1_2w_male.sql.log
│   │   ├── Q1_3w_female.sql.log
│   │   ├── Q1_3w_male.sql.log
│   │   ├── Q2_1w_female.sql.log
│   │   ├── Q2_1w_male.sql.log
│   │   ├── Q2_2w_female.sql.log
│   │   ├── Q2_2w_male.sql.log
│   │   ├── Q2_3w_female.sql.log
│   │   ├── Q2_3w_male.sql.log
│   │   ├── Q3_1w_female.sql.log
│   │   ├── Q3_1w_male.sql.log
│   │   ├── Q3_2w_female.sql.log
│   │   ├── Q3_2w_male.sql.log
│   │   ├── Q3_3w_female.sql.log
│   │   ├── Q3_3w_male.sql.log
│   │   ├── Q4_1w_female.sql.log
│   │   ├── Q4_1w_male.sql.log
│   │   ├── Q4_2w_female.sql.log
│   │   └── Q4_2w_male.sql.log
│   └── OLAP_NuoDB_TFIDF
│       ├── Q1_1w_female.sql.log
│       ├── Q1_1w_male.sql.log
│       ├── Q1_2w_female.sql.log
│       ├── Q1_2w_male.sql.log
│       ├── Q1_3w_female.sql.log
│       ├── Q1_3w_male.sql.log
│       ├── Q2_1w_female.sql.log
│       ├── Q2_1w_male.sql.log
│       ├── Q2_2w_female.sql.log
│       ├── Q2_2w_male.sql.log
│       ├── Q3_1w_female.sql.log
│       ├── Q3_1w_male.sql.log
│       ├── Q3_2w_female.sql.log
│       ├── Q3_2w_male.sql.log
│       ├── Q4_1w_female.sql.log
│       ├── Q4_1w_male.sql.log
│       ├── Q4_2w_female.sql.log
│       ├── Q4_2w_male.sql.log
│       ├── Q4_3w_female.sql.log
│       └── Q4_3w_male.sql.log
└── TopK_keywords
    ├── OLAP_NuoDB_Okapi
    │   ├── Q1_female.sql.log
    │   ├── Q1_male.sql.log
    │   ├── Q2_female.sql.log
    │   ├── Q2_male.sql.log
    │   ├── Q3_female.sql.log
    │   ├── Q3_male.sql.log
    │   ├── Q4_female.sql.log
    │   └── Q4_male.sql.log
    └── OLAP_NuoDB_TFIDF
        ├── Q1_female.sql.log
        ├── Q1_male.sql.log
        ├── Q2_female.sql.log
        ├── Q2_male.sql.log
        ├── Q3_female.sql.log
        ├── Q3_male.sql.log
        ├── Q4_female.sql.log
        └── Q4_male.sql.log
```

Now you may close the containers:

```
docker compose down
or
docker-compose -f docker-compose-distributed.yml down
```

And repeat the process for the other data sets.