CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR NOT NULL   
);
CREATE TABLE Term (
    term VARCHAR PRIMARY KEY,
    num_chars INT NOT NULL 
);
CREATE TABLE Document (
    document_id INT PRIMARY KEY, 
    category_id INT NOT NULL,
    doc_text VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    num_chars int NOT NULL,
    recorded_at date NOT NULL,

    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);
CREATE TABLE DocumentTerm (
    document_id INT, 
    term VARCHAR,
    count INT NOT NULL,

    FOREIGN KEY (document_id) REFERENCES Document(document_id),
    FOREIGN KEY (term) REFERENCES Term(term)
);