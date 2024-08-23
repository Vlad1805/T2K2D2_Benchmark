-- Create genders table
CREATE TABLE genders (
    id INTEGER PRIMARY KEY,
    type VARCHAR(8)
);

-- Create authors table
CREATE TABLE authors (
    id BIGINT PRIMARY KEY,
    id_gender INTEGER,
    firstname VARCHAR(32),
    lastname VARCHAR(32),
    age INTEGER,
    FOREIGN KEY (id_gender) REFERENCES genders(id)
);

-- Create geo_location table
CREATE TABLE geo_location (
    id INTEGER PRIMARY KEY,
    X DOUBLE,
    Y DOUBLE
);

-- Create documents table
CREATE TABLE documents (
    id BIGINT PRIMARY KEY,
    id_geo_loc INTEGER,
    raw_text TEXT,
    lemma_text TEXT,
    clean_text TEXT,
    document_date TIMESTAMP,
    FOREIGN KEY (id_geo_loc) REFERENCES geo_location(id)
);

-- Create words table
CREATE TABLE words (
    id INTEGER PRIMARY KEY,
    word VARCHAR(256)
);

-- Create vocabulary table
CREATE TABLE vocabulary (
    id_document INTEGER,
    id_word INTEGER,
    count INTEGER,
    tf DOUBLE,
    PRIMARY KEY (id_document, id_word),
    FOREIGN KEY (id_document) REFERENCES documents(id),
    FOREIGN KEY (id_word) REFERENCES words(id)
);

-- Create documents_authors table to handle the relationship between authors and documents
CREATE TABLE documents_authors (
    id_author INTEGER,
    id_document INTEGER,
    PRIMARY KEY (id_author, id_document),
    FOREIGN KEY (id_author) REFERENCES authors(id),
    FOREIGN KEY (id_document) REFERENCES documents(id)
);