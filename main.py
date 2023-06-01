from bs4 import BeautifulSoup
import requests

with open('source.html', 'r', encoding='utf-8') as file:
    page_content = file.read()

# url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"
# page = requests.get(url)

soup = BeautifulSoup(page_content, "html.parser")
results = soup.find('section', class_="courses-wrapper")

grade = results.find('h3', class_="c12638")
print(grade.string)
div = results.find_all('div', class_="course-details")

for div_tags in div:
    ul_tags = div_tags.find_all('ul')
    for ul in ul_tags:
        subsection = ul.find_previous_sibling('h4')
        if subsection:
            print(subsection.string)
        else:
            print("No preceding h4 sibling found for ul.")
        
        for li in ul.find_all('li'):
            print(li.string)
