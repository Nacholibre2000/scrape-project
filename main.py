from bs4 import BeautifulSoup
import requests

with open('source.html', 'r', encoding='utf-8') as file:
  page_content = file.read()

# url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"
# page = requests.get(url)

soup = BeautifulSoup(page_content, "html.parser")
result = soup.find('div', class_="content")

central_contents = result.find('section')
course_requirements = central_contents.find_next_sibling('section')

for central_contents_tags in central_contents.find_all(
    'div', class_="course-details"):
  grade = central_contents_tags.find('h3')
  print(grade.string)
  ul_tags = central_contents_tags.find_all('ul')
  for ul in ul_tags:
    subsection = ul.find_previous_sibling('h4')
    if subsection:
      print(subsection.string)
    else:
      print("No preceding h4 sibling found for ul.")
    for central_content in ul.find_all('li'):
      print(central_content.string)

for articles in course_requirements.find_all('article'):
  grade = articles.find('h3')
  print(grade.string)
  for paragraph in articles.find('div', class_="course-details").find_all('p'):
    paragraph_text = paragraph.get_text()
    sentences = paragraph_text.split('. ')
    #sentences = list(filter(None, sentences))
    for sentence in sentences:
      print(sentence)

#for central_requirement_tags in central_requirements.find_all('div', class_="course-details")

#div = result.find_all('div', class_="course-details")

# for div_tags in div:
#   grade = div_tags.find('h3')
#   print(grade.string)
#   ul_tags = div_tags.find_all('ul')
#   for ul in ul_tags:
#     subsection = ul.find_previous_sibling('h4')
#     if subsection:
#       print(subsection.string)
#     else:
#       print("No preceding h4 sibling found for ul.")
#     for central_content in ul.find_all('li'):
#       print(central_content.string)
