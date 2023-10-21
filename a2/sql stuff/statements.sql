INSERT INTO Category (category_id,category_name) VALUES ('cat_id_int','Example Category');

INSERT INTO Term (term, num_chars) VALUES ('term',4);

INSERT INTO Document (document_id,category_id,doc_text,title, num_chars ,
                        recorded_at) VALUES
                         ('some_unqiue_doc_id_int','some_existing_cat_id_int','text_content_str','document_title_str',
                            'character_count_int','date_recorded_dateDataStructure'
                          );
INSERT INTO DocumentTerm(document_id,term,count ) VALUES ('document_id_int','term','count_int')
