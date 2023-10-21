from psycopg2 import connect

def main():
    connection=connect(database="a2",user="franserr",host="localhost")
    cur = connection.cursor()
    print(f"the number of documents: {str(numOfDocuments(cur))}" )
    print(f"the number of sport documents: {str(numOfSportDocuments(cur))}" )
    print(f"the number of terms: {str(numOfTerms(cur))}" )
    print(f"the number of terms in arizona document (counting repetitions): {str(totalNumOfTermsArizona(cur))}" )
    print(f"the number of terms in seasons docs(counting repetitions): {str(totalNumOfTermsSeasons(cur))}" )
    print(f"the number of times the term 'months' appeared in D (counting repetitions): {str(termCountMonths(cur))}" )
    print(largestDocument(cur))
    print(mostFrequentTerm(cur))
#recall we need to use a single query for all of these! 
# a.  How many documents are in D?
def numOfDocuments(cur)->int:
    cur.execute("SELECT COUNT(*) FROM Document")
    res=cur.fetchone()[0]
    return int(res)
# b. How many documents are in D from the category "Sports"? Requirement: query the
#       tables by using the category name.
def numOfSportDocuments(cur)->int:
    cur.execute("SELECT COUNT(*) FROM Document AS D INNER JOIN Category AS C ON D.category_id = C.category_id "\
                 "WHERE C.category_name = 'Sports' ")
    res=cur.fetchone()[0]
    return int(res)
# c. How many distinct terms are in D?
def numOfTerms(cur)->int:
    cur.execute("SELECT COUNT (*) FROM Term")
    res=cur.fetchone()[0]
    return int(res)
# d. How many terms (considering repetitions) are in the document “Arizona”? Requirement:
#       query the tables by using the document title.
def totalNumOfTermsArizona(cur)->int:
    cur.execute("SELECT SUM(DT.count) FROM Document AS D INNER JOIN DocumentTerm AS DT ON D.document_id = DT.document_id" +
            " WHERE D.title = 'Arizona'")
    return int(cur.fetchone()[0])
# e. How many terms (considering repetitions) are linked to the category "Seasons"?
#       Requirement: query the tables by using the category name.
def totalNumOfTermsSeasons(cur)->int:
    cur.execute("SELECT SUM(DT.count) FROM Document AS D INNER JOIN DocumentTerm AS DT ON D.document_id = DT.document_id" +
            " INNER JOIN Category AS C ON D.category_id=C.category_id WHERE C.category_name = 'Seasons'")
    return int(cur.fetchone()[0])
# f. How many times (considering repetitions) does the term "months" occur in D?
def termCountMonths(cur)->int:
    cur.execute("SELECT SUM(count) FROM DocumentTerm AS DT WHERE DT.term= 'months'")
    return int(cur.fetchone()[0])
# g. What is the largest document (more terms - considering repetitions)? Requirement:
#       output the document title and its corresponding number of terms.
def largestDocument(cur)->str:

    cur.execute("SELECT D.title, SUM(DT.count) FROM Document AS D INNER JOIN DocumentTerm AS DT ON D.document_id"+
                " = DT.document_id GROUP BY D.document_id ORDER BY SUM(DT.count) DESC LIMIT 1")
    record=cur.fetchone()
    title=record[0]
    term_count=record[1]
    return title+" has the largest amount of terms. Term Count: "+ str(term_count)
# h. What is the most frequent term in D (considering the number of distinct documents)?
#       Requirement: output the term and its corresponding occurrences.

def mostFrequentTerm(cur)->str:
    cur.execute("SELECT term, SUM(DT.count) FROM DocumentTerm AS DT "+
                "GROUP BY DT.term ORDER BY SUM(DT.count) DESC LIMIT 1")
    record=cur.fetchone()
    term=record[0]
    term_count=record[1]
    return "'"+term+"' was the most frequently used term. Count: "+ str(term_count)

main()