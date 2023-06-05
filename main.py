from bs4 import BeautifulSoup
import requests

with open('source.html', 'r', encoding='utf-8') as file:
  page_content = file.read()

# url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"
# page = requests.get(url)

soup = BeautifulSoup(page_content, "html.parser")
results_content = soup.find('section', class_="courses-wrapper")
results_requirements = results_content.find_next_sibling('section')

div = results_content.find_all('div', class_="course-details")
# ul = div.find('ul')
# ul_sibling = ul.find_previous_sibling('h4')
# print(ul_sibling.string)
# for child in ul.children:
#         print(child.string)

for div_tags in div:
  grade = div_tags.find('h3')
  print(grade.string)
  ul_tags = div_tags.find_all('ul')
  for ul in ul_tags:
    subsection = ul.find_previous_sibling('h4')
    if subsection:
      print(subsection.string)
    else:
      print("No preceding h4 sibling found for ul.")

    for li in ul.find_all('li'):
      print(li.string)
for
#   for grade in grades:
#     print(f"Grade:{grade.text}")
#   subsection_list = result.find_all('h4', class_="c12638")
#   for subsection in subsection_list:
#     print(f"Subsection: {subsection.text}")
#   central_content_list = result.find_all('li')
#   for central_content in central_content_list:
#     print(f"Central content: {central_content.text}")

#  print(f"Subsection:{subsection.text}")
#  print(f"Central content:{course_requirement.text}")

#print(grades)
#<h4 class="c12638">Att leva tillsammans</h4>
#for ul in central_content:
## OLDS

#coursedetails = soup.find_all("div", {"class": "course-details"})

#subsection = soup.find_all('h4', class_="c12638") # to find subsection
#print(subsection) # to find subsection

#<h3 class="c12638"> Är årskurs
#<h4 class="c12638"> Är subsection
#<li> Är alla centrala innehåll
#grades = coursedetails.find_all("h3", {"class": "c12638"})

#print(coursedetails)
#print(soup)

#grade = soup.find_all('h3', class_="c12638") # to find grade
# print(grade) # to find grade
