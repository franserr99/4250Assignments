from bs4 import BeautifulSoup
import re
with open('q2.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# print(soup.prettify())

# print("Here is the title:", soup.head.title.get_text())
# question 1
print("Question 1:")
title_tag = soup.find("title")
if title_tag:
    print("Here is the title: ", title_tag.get_text())
else:
    print("Not able to find the title")
# question 2
print("\nQuestion 2:")
ul_tag = soup.find("ul")
li_tags = ul_tag.find_all("li")
index = -1

for i, tag in enumerate(li_tags):
    if "To show off" in tag.get_text():
        index = i
if index != -1:
    target_outter_tag = li_tags[index]
    inner_tags = target_outter_tag.find("ol").find_all("li")
    print(inner_tags[1].get_text())
# question 3 : All cells of Row 2. Use the HTML tags to do this search.
print("\n Question 3:")

second_row = soup.find("table").find("tr", {'class': 'tutorial2'})

cells = ""
for cell in second_row.children:
    # do some kind of check to see if you can go into the children
    # and print out the cells?
    cells += cell.get_text() + " "
    # the last one has an image tag im not picking up :
    # <img src=http://www.ccc.com/badge3.gif></td>
print("Here are the cells of the second row: ", cells)

# question 4: All h2 headings that includes the word “tutorial”.
# Use the HTML tags to do this search

h2_tags = soup.find_all("h2")
for tag in h2_tags:
    if "tutorial" in tag.get_text().lower():
        print(tag.get_text())

# question 5: All text that includes the “HTML” word. Use the HTML text to do this search.
regex = re.compile("HTML")
html_texts = soup.find_all(text=regex)
print("Here are all the text that contain HTML in it: \n")
for text in html_texts:
    print(text.get_text().strip())
    print()
# question 6 : All cells’ data from the first row of the table. Use the HTML tags to do this search.
for cell_tag in soup.find("tr", {'class': 'tutorial1'}).children:
    print(cell_tag.get_text())

# question 7 : All images from the table. Use the HTML tags to do this search.

imgs = soup.find("table").find_all("img")
print("Here are the images in the table:")
for image_tag in imgs:
    print(image_tag.attrs.get('src'))

