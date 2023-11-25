from bs4 import BeautifulSoup
import re
try:
    with open('q2.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
except FileNotFoundError:
    print("File not found")
    exit()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()
soup = BeautifulSoup(html_content, 'html.parser')

# question a: Find the title, used tags for the search
print("part a:")
title_tag = soup.find("title")
if title_tag:
    print("Here is the title: ", title_tag.get_text())
else:
    print("Not able to find the title")
# question b
# NOTE TO PROF: I assume you wanted us to get the tags then do our own search
#               So I use the structure, do a match on text content
#               Then I select the second element
print("\npart b:")
ul_tag = soup.find("ul")
if ul_tag:
    li_tags = ul_tag.find_all("li")
    index = -1
    if li_tags:
        for i, tag in enumerate(li_tags):
            if "To show off" in tag.get_text():
                index = i
                break
        if index != -1 and li_tags[index].find("ol"):
            target_outter_tag = li_tags[index]
            inner_tags = target_outter_tag.find("ol").find_all("li")
            if len(inner_tags) > 1:
                for tag in inner_tags:
                    if "To my friends" in tag.get_text():
                        print(tag.get_text())
                        break
# question c : All cells of Row 2. Use the HTML tags to do this search.
# NOTE TO PROF: i assumed you didnt want us to get the img src here
#               since you asked that that in another question
print("\npart c:")
second_row = soup.find("table").find("tr", {'class': 'tutorial2'})
cells = ""
if second_row:
    for cell in second_row.children:
        cells += cell.get_text() 
    print("Here are the cells of the second row: \n", cells)
# they will print on different lines for readability,
# if you want it all on a single line then do cell.get_text().strip()

# question d: All h2 headings that includes the word “tutorial”.
# Use the HTML tags to do this search
print("\npart d:")
h2_tags = soup.find_all("h2")
if h2_tags:
    for tag in h2_tags:
        if tag:
            if "tutorial" in tag.get_text().lower():
                print(tag.get_text())
# question e: All text that includes the “HTML” word.
# Use the HTML text to do this search.
print("\npart e:")
regex = re.compile("HTML")
html_texts = soup.find_all(string=regex)
print("Here are all the text that contain HTML in it: \n")
if html_texts:
    for text in html_texts:
        print(text.get_text().strip())
# question f : All cells’ data from the first row of the table.
#  Use the HTML tags to do this search.
# NOTE TO PROF: i assumed you didnt want us to get the img src here
#               since you asked that that in another question
print("\npart f:")
cells = ""
for cell_tag in soup.find("tr", {'class': 'tutorial1'}).children:
    cells += cell_tag.get_text()
print(cells)
# question g : All images from the table. Use the HTML tags to do this search.
print("\npart g:")
imgs = soup.find("table").find_all("img")
print("Here are the images in the table:")
for image_tag in imgs:
    print(image_tag.attrs.get('src'))
