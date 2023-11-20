from bs4 import BeautifulSoup
from pymongo import MongoClient


def persistProfessors():
    target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'
    try:
        client = MongoClient('mongodb://localhost:27017/')
    except Exception:
        print("not able to connect to db")

    pages_collection = client['corpus']['pages']
    professor_collection = client['corpus']['professors']
    query = {"_id": target_url}
    page_data = pages_collection.find_one(query)

    if page_data:
        html = page_data['html']
        soup = BeautifulSoup(html, 'html.parser')
        professors = soup.find(
            'section', {'id': 's0', 'class': 'text-images'}).find_all('div')
        for professor in professors:
            # there are empty lines for readability,
            #  check if the children are actual tags (no text nodes)
            if professor.name and professor.find('p'):
                name = professor.find('h2').get_text().strip()
                print(name)
                print()
                info = {}

                for prof_info in professor.find_all("strong"):
                    strong_content = str(prof_info.get_text()).split(":")[
                        0].lower().strip()

                    if (strong_content == 'web'):
                        info[strong_content] = prof_info.find_next_sibling(
                            "a").get('href').strip()
                    elif (strong_content == 'email'):
                        info[strong_content] = prof_info.find_next_sibling(
                            "a").get_text().strip()
                    else:
                        content = str(
                            prof_info.next_sibling.get_text()).strip()
                        if content.startswith(":"):
                            content = content.replace(":", "").strip()
                        content = content.encode(
                            'utf-8').decode('ascii', 'ignore')
                        info[strong_content] = content

                prof = {'name': name, 'title': info['title'],
                        'phone': info['phone'], 'office': info['office'],
                        'email': info['email'], 'website': info['web']}
                professor_collection.insert_one(prof)

    else:
        print("not in db:", target_url)


persistProfessors()
