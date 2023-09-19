#-------------------------------------------------------------------------
# AUTHOR: Francisco Serrano
# FILENAME: search_engine.py
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2.5hrs (started at 7:30pm ended at 10pm)
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
from math import log10
documents = []
labels = []
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
keys=list(steeming.keys())
###### helper functions######
def do_stemming(string):
    line=string.split(" ")
    new_line=[]
    for word in line:
        if(word in keys):
            new_line.append(steeming[word])
        else:
            new_line.append(word)
    return new_line
def stop_word_removal(string):
    line=string.split(" ")
    new_line=[]
    for word in line:
        if(word not in stopWords):
            new_line.append(word)
    return new_line
#############################################

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])
print("\n\nThe documents as they were read:")
print(documents)

#Conduct stopword removal.
#--> add your Python code here
new_docs=[]
for document in documents:
    new_docs.append(" ".join(stop_word_removal(document)))   
documents=new_docs
print("\n\ndocuments after removing stopwords")
print(documents)    
#Conduct stemming.
#--> add your Python code here
new_docs=[]
for document in documents:
    new_docs.append(" ".join(do_stemming(document)))
documents=new_docs
print("\n\ndocuments after stemming")
print(documents)
#Identify the index terms.
#--> add your Python code here
terms = []
for document in documents:
    line=document.split(" ")
    for word in line:
        if(word not in terms):
            terms.append(word)
print("\n\nUnique terms identified over the set of docs")
print(terms)
print(f"\n\nthis many unqiue terms identified:{len(terms)}")
#Build the tf-idf term weights matrix.
#--> add your Python code here
docMatrix = []
#get document frequency for each term
document_frequency={term:0 for term in terms}
for document in documents:
    line=document.split(" ")
    seen=set()
    for word in line:
        if(word in terms and word not in seen ):
            document_frequency[word]+=1
            seen.add(word)
print("\n\ndocument frequency by term:")
print(document_frequency)

#get term count, then compute tf-idf
num_of_docs=len(documents)
for document in documents:
    dWeight_map={}
    line=document.split(" ")
    #get term count
    for word in line:
        if word in dWeight_map:
            dWeight_map[word]+=1
        else:
            dWeight_map[word]=1
    print(f"\n\nterm count for this doc ' {document} ' :")
    print(dWeight_map)
    #convert into an ordered list determined by terms arr
    dWeight_Matrix=[]
    for term in terms:
        #term was not in the line
        if(term not in dWeight_map):
            dWeight_Matrix.append(0)
        else:
            dWeight_Matrix.append(dWeight_map[term]/len(line))
    #used the matrix for term freq now we convert to tf-idf and finish it off
    final_weights=[]
    for index,weight in enumerate(dWeight_Matrix):
        final_weights.append(weight* log10(num_of_docs/document_frequency[terms[index]]))
    docMatrix.append(final_weights)
print("\n\nthis is the tf-idf matrix:")
print(docMatrix[0])
print(docMatrix[1])
print(docMatrix[2])
#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docScores = []

query="cats and dogs"
#remove stop words and stemming
query=" ".join(stop_word_removal(query))
query=do_stemming(query)
print(f"\n\nThis is the query after stopword removal and stemming : \n \t\t{query}")
print("******")
query_terms=query
query_binary_vector=[]
for term in terms:
    if term in query_terms:
        query_binary_vector.append(1)
    else:
        query_binary_vector.append(0)

for record in docMatrix:
    score=0
    for q,d in zip(query_binary_vector,record):
        score+=q*d
    docScores.append(score)

# Display the sorted documents and their scores
for i,score in enumerate(docScores):
    print(f"Document {i+1} Score: {score}")

#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here
returned_scores=[]
for score in docScores:
    if(score>0.1):
        returned_scores.append(score)
strippedLabel=[term.strip() for term in labels]
print(strippedLabel)
labels=strippedLabel
#find out how many records/documents had the R label
actually_relevant= sum (1 if term=='R' else 0 for term in labels)
print(actually_relevant)
#compare against provideded labels, check how many retrieved/returned were actually relevant
retrieved_relevant= sum (1 if (term=='R' and docScores[i]>0.1) else 0 for i,term in enumerate(labels))
#percision: retrieved relevant documents/number of retrieved documents
percision=retrieved_relevant/len(returned_scores)
print(f"percision is {percision}")
recall=retrieved_relevant/actually_relevant
#recall: retrieved relevant documents/number of relevant documents
print(f"recall is {recall}")