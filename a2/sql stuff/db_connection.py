#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: 4hr
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python librarie
from psycopg2 import connect,DatabaseError,sql
import string

def connectDataBase():
    '''
    Function used to create the connection object. Tables are also created here if they aren't already in the db
    '''
    #init to none, avoid errors on check outside of try's scope
    cur = None
    connection = None
    try:
        connection = connect(database="corpus", user="franserr", host="localhost")
        #need a cursor to check for table creation and 
        cur = connection.cursor()
        # List of table create statements
        create_statements = [
            '''
            CREATE TABLE IF NOT EXISTS Category (
                category_id INT PRIMARY KEY,
                category_name VARCHAR NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Term (
                term VARCHAR PRIMARY KEY,
                num_chars INT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Document (
                document_id INT PRIMARY KEY,
                category_id INT NOT NULL,
                doc_text VARCHAR NOT NULL,
                title VARCHAR NOT NULL,
                num_chars INT NOT NULL,
                recorded_at DATE NOT NULL,
                FOREIGN KEY (category_id) REFERENCES Category(category_id)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS DocumentTerm (
                document_id INT NOT NULL,
                term VARCHAR NOT NULL,
                count INT NOT NULL,
                FOREIGN KEY (document_id) REFERENCES Document(document_id),
                FOREIGN KEY (term) REFERENCES Term(term)
            );
            '''
        ]
        # execute the commands
        for create_statement in (create_statements):
            cur.execute(create_statement)
        # commit changes
        connection.commit()
    except DatabaseError as db_error:
        print("Database error occurred:", db_error)
        #roll it back, other transactions hit error if this doesnt happen
        if connection:
            connection.rollback()
    except Exception as error:
        print("An error occurred:", error)
    finally:
        #close the cursor if it was created
        if cur:
            cur.close()
    return connection
def createCategory(cur, catId, catName):
    #insert the category record
    cur.execute("INSERT INTO Category (category_id,category_name) VALUES (%s,%s)",(int(catId),catName))
def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # find category_id from the name
    category_name=docCat
    cur.execute("SELECT category_id FROM Category WHERE category_name= %s",(category_name,))
    record=cur.fetchone()
    cat_id=record[0]

    ################ start of helper functions ##################
    def remove_punctuation(input_string):
        return ''.join(letter for letter in input_string if letter not in string.punctuation)
    def term_in_db(term,cur) -> bool:
        cur.execute("SELECT * FROM Term WHERE term = %s",(term,))
        res=cur.fetchone()
        if(res): #check to see a result was returned
            return True
        return False
    def add_term(term,num_chars,cur):
        cur.execute("INSERT INTO Term (term,num_chars) VALUES (%s,%s)", (term,int(num_chars)))
    def add_document_term(cur,term,doc_id,count):
        cur.execute("INSERT INTO DocumentTerm(document_id,term, count) VALUES (%s,%s,%s)", (int(doc_id),term,int(count)))
    ############# end of helper functions ##################

    # discard the spaces and punctuation marks
    text_no_punc=remove_punctuation(docText)
    tokens=text_no_punc.lower().split(" ")

    # find unique terms over document, note their occurences
    # keep track of the total character count for the document
    character_count=0
    terms={}
    for token in tokens:
        #add length of a single word (we're counting duplicates so no condition)
        character_count+=len(token)
        #count occurences
        if token not in terms:
            terms[token]=1
        else:
            terms[token]+=1
    #create the document record
    cur.execute("INSERT INTO Document (document_id,category_id,doc_text,title, num_chars ,"\
                        "recorded_at) VALUES"\
                         "(%s,%s,%s,%s,%s,%s);",(int(docId),int(cat_id),docText,docTitle,int(character_count), docDate) )
    
    #iterate again now we have the term counts over the doc
    for term,count in terms.items():
        # check if the term already exists in the database
        if(not term_in_db(term,cur)):
            # if does not exist, insert it into the database
            add_term(term=term,num_chars=len(term),cur=cur)
        # insert the term and its corresponding count into the database
        add_document_term(cur, term,doc_id=docId,count=count)
def deleteDocument(cur, docId):
    # find all records in inverted index table
    cur.execute("SELECT * FROM DocumentTerm WHERE document_id = %s",(int(docId),))
    records=cur.fetchall()
    terms=[]
    #transform to python ds (i think you can do this using built in functions but I want to format)
    for document_id,term,count in records:
        #save the info to make later steps easier
        terms.append({'term':term,'count':count,'document_id':document_id})
    #get rid of the inverted index table entries for the document
    cur.execute("DELETE FROM DocumentTerm WHERE document_id = %s",(int(docId),))
    #find all records in the inverted index table that were associated with the document
    for term in terms:
        cur.execute("SELECT * FROM DocumentTerm WHERE term = %s",(term['term'],))
        records=cur.fetchall()
        #if it is not longer associated to other documents, get rid of the term
        if not records:
            cur.execute("DELETE FROM Term WHERE term = %s", (term['term'],))
    # now you can safely delete the document
    cur.execute("DELETE FROM Document WHERE document_id = %s",(int(docId),))
def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    # delete the doc
    deleteDocument(cur=cur,docId=docId)
    # create new one with updated info
    createDocument(cur=cur,docId=docId,docText=docText,docTitle=docTitle,docDate=docDate,docCat=docCat)
def getIndex(cur):
    cur.execute("SELECT * FROM DocumentTerm")
    records=cur.fetchall()
    terms={}

    for document_id,term,count in records:
        if term not in terms:
            terms[term]=[]
        #get the document name
        cur.execute("SELECT * FROM Document WHERE document_id = %s", (document_id,))
        name=cur.fetchone()[3]
        terms[term].append((name, count))

    index={}
    for term,info in terms.items():
        # if len(info)>1:   
        n=len(info)
        for i in range(n):
            if term not in index:
                index[term]=info[i][0]+": "+ str(info[i][1])
            else:
                index[term]+=info[i][0]+": "+ str(info[i][1])
            if(i<n-1):
                index[term]+=", "
    return index
