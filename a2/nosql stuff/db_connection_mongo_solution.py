from pymongo import MongoClient
import string
from datetime import datetime
def connectDataBase():
    # Create a database connection object 
    client = MongoClient(host=['localhost:27017'])
    db=client['corpus']
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    category_name=docCat
    # ############### start of helper functions ##################
    def remove_punctuation(input_string):
        return ''.join(letter for letter in input_string if letter not in string.punctuation)
    def term_in_db(term,col) -> bool:
            count=col.count_documents({"term":term})
            return count > 0
    def add_term(term,num_chars,col):
        document={"term":term, "num_chars":int(num_chars), "documents":[]}
        col.insert_one(document)
    def append_document(col, document,term):
        #first find if the term already has that document, if so then just return
        # it does not enforce constraints in the embedded 
        # document array so you need to do something else 
        #find the term's document
        term_doc=col.find_one({"term":term,"documents._id":int(document['_id'])})
        if term_doc:
            print("it was already added!")
            return None
        query= {"term":term}
        #add to the array
        values={
            "$push": {
                "documents": document
            }
        }
        col.update_one(query,values)
    ############# end of helper functions ##################

    text_no_punc=remove_punctuation(docText)
    tokens=text_no_punc.lower().split(" ")
    character_count=0
    terms={}
    #loop for the character count and term count
    for token in tokens:
        character_count+=len(token)
        if token not in terms:
            terms[token]=1
        else:
            terms[token]+=1
    

    #iterate again now we have the term counts
    for term,count in terms.items():
        # 3.2 For each term identified, check if the term already exists in the database
        if(not term_in_db(term,col)):
            # 3.3 In case the term does not exist, insert it into the database
            add_term(term=term,num_chars=len(term),col=col)
        # 4.3 Insert the term and its corresponding count into the database
        document= {
            "_id":int(docId),
            "category": category_name,
            "text": docText,
            "title": docTitle,
            "num_chars":int(character_count),
            "date": datetime.strptime(docDate, "%Y-%m-%d"),
            "term_count":int(count)
        }
        append_document(col=col,document=document,term=term)




def deleteDocument(col, docId):
    
    # i only want to delete the nested object, not the entire term document
    # i need to update the document then use an operator for the embedded docs
    # there is not query object since i want to iterate over every term document

    #keep a list of the terms before we delete the embedded documents
    terms= list (col.find({"documents._id":int(docId)}))
    update= { 
        "$pull": {
            "documents": { 
                "_id": int(docId)
            }
        }
    }
    col.update_many({},update)
    # # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    for term_doc in terms:
        term_str=term_doc["term"]
        updated_term_doc=col.find_one({"term":term_str})
        if(updated_term_doc):
            if len (updated_term_doc["documents"])==0:
                col.delete_one({"term":term_str})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(col=col,docId=docId)
    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(col=col,docId=docId,docText=docText,docTitle=docTitle,docDate=docDate,docCat=docCat)
def getIndex(col):
    
    

    terms=list(col.find())
    index={}

    for term_document in terms:
        term=term_document["term"]
        n=len(term_document["documents"])

        for i,document in enumerate(term_document["documents"]):
            if term not in index:
                index[term]=document["title"] + ": "+str(document["term_count"])
            else:
                index[term]+=document["title"] + ": "+str(document["term_count"])
            if(i<n-1):
                index[term]+=", "
    return index
    # index={}
    # for term,info in terms.items():
    #     # if len(info)>1:
    #     #     
    #     n=len(info)
    #     for i in range(n):
    #         if term not in index:
    #             index[term]=info[i][0]+": "+ str(info[i][1])
    #         else:
    #             index[term]+=info[i][0]+": "+ str(info[i][1])
    #         if(i<n-1):
    #             index[term]+=", "
    # return index

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here