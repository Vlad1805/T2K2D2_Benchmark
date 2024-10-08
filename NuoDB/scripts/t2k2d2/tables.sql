-- Create document_dimension table
CREATE TABLE document_dimension (
    id_document BIGINT PRIMARY KEY,
    raw_text TEXT,
    clean_text TEXT,
    lemma_text TEXT
);

-- Create author_dimension table
CREATE TABLE author_dimension (
    id_author BIGINT PRIMARY KEY,
    firstname VARCHAR(32),
    lastname VARCHAR(32),
    gender VARCHAR(16),
    age INTEGER
);

-- Create time_dimension table
CREATE TABLE time_dimension (
    id_time INTEGER PRIMARY KEY,
    minute INTEGER,
    hour INTEGER,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    full_date DATETIME
);

-- Create location_dimension table
CREATE TABLE location_dimension (
    id_location INTEGER PRIMARY KEY,
    X INTEGER,
    Y INTEGER
);

-- Create word_dimension table
CREATE TABLE word_dimension (
    id_word INTEGER PRIMARY KEY,
    word VARCHAR(256)
);

-- Create document_fact table
CREATE TABLE document_facts (
    id_document BIGINT,
    id_author BIGINT,
    id_time INTEGER,
    id_location INTEGER,
    id_word INTEGER,
    count FLOAT,
    tf FLOAT,
    PRIMARY KEY (id_document, id_author, id_time, id_location, id_word),
    FOREIGN KEY (id_document) REFERENCES document_dimension(id_document),
    FOREIGN KEY (id_author) REFERENCES author_dimension(id_author),
    FOREIGN KEY (id_time) REFERENCES time_dimension(id_time),
    FOREIGN KEY (id_location) REFERENCES location_dimension(id_location),
    FOREIGN KEY (id_word) REFERENCES word_dimension(id_word)
);
