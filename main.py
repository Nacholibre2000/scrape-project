from bs4 import BeautifulSoup
import requests
import csv

with open('source.html', 'r', encoding='utf-8') as file:
  page_content = file.read()

# url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"
# page = requests.get(url)

#groundwork
soup = BeautifulSoup(page_content, "html.parser")
result = soup.find('div', class_="content")

central_contents = result.find('section')
course_requirements = central_contents.find_next_sibling('section')

# Dictionaries to store data
grade_data = {}
subsection_data = {}
central_content_data = {}
central_requirement_data = {}

# Keeping track of ids
grade_id = 1
subsection_id = 1
central_content_id = 1
central_requirement_id = 1

# List to keep track of original subsections
original_subsections = []
original_sentences = []

for idx, central_contents_tags in enumerate(central_contents.find_all(
    'div', class_="course-details"),
                                            start=1):
  grade = central_contents_tags.find('h3').string
  if grade not in grade_data:
    grade_data[grade] = grade_id
    grade_id += 1

  grade_id_current = grade_data[grade]

  ul_tags = central_contents_tags.find_all('ul')
  for ul in ul_tags:
    subsection = ul.find_previous_sibling('h4')
    if subsection:
      subsection = subsection.string
      # append grade if the subsection has been seen before
      if subsection in original_subsections:
        subsection = subsection + " (" + grade + ")"
      else:
        original_subsections.append(subsection)

      if subsection not in subsection_data:
        subsection_data[subsection] = (subsection_id, grade_id_current)
        subsection_id += 1
    else:
      print("No preceding h4 sibling found for ul.")

    subsection_id_current = subsection_data[subsection][0]

    for central_content in ul.find_all('li'):
      central_content = central_content.string
      if central_content not in central_content_data:
        central_content_data[central_content] = (central_content_id,
                                                 subsection_id_current)
        central_content_id += 1

for idx, articles in enumerate(course_requirements.find_all('article'), start=1):
    grade = articles.find('h3').string

    if grade == "Kriterier för bedömning av godtagbara kunskaper i slutet av årskurs 3":
        grade = "I årskurs 1–3"

    if grade == "Betygskriterier för slutet av årskurs 6":
        grade = "I årskurs 4–6"

    if grade == "Betygskriterier för slutet av årskurs 9":
        grade = "I årskurs 7–9"
      
    if grade not in grade_data:
        grade_data[grade] = grade_id
        grade_id += 1
    
    grade_id_current = grade_data[grade]
    
    paragraphs = articles.find('div', class_="course-details").find_all('p')
    for paragraph in paragraphs:
        sentences = paragraph.get_text().split('. ')
        for central_requirement in sentences:
            # append grade if the sentence has been seen before
            if central_requirement in original_sentences:
                central_requirement = central_requirement + "-" + grade
            else:
                original_sentences.append(central_requirement)
                
            if central_requirement not in central_requirement_data:
                central_requirement_data[central_requirement] = (central_requirement_id, grade_id_current)
                central_requirement_id += 1

# Create and write to CSV files
with open('grade_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "grade"])
  for key, value in grade_data.items():
    writer.writerow([value, key])

with open('subsection_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "subsection", "foreign_id_grades"])
  for key, value in subsection_data.items():
    writer.writerow([value[0], key, value[1]])

with open('central_content_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "central_content", "foreign_id_subsections"])
  for key, value in central_content_data.items():
    writer.writerow([value[0], key, value[1]])

with open('central_requirement_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "sentence", "foreign_id_grades"])
    for key, value in central_requirement_data.items():
        writer.writerow([value[0], key, value[1]])

# standard content code
# for central_contents_tags in central_contents.find_all(
#     'div', class_="course-details"):
#   grade = central_contents_tags.find('h3')
#   print(grade.string)
#   ul_tags = central_contents_tags.find_all('ul')
#   for ul in ul_tags:
#     subsection = ul.find_previous_sibling('h4')
#     if subsection:
#       print(subsection.string)
#     else:
#       print("No preceding h4 sibling found for ul.")
#     for central_content in ul.find_all('li'):
#       print(central_content.string)

# standard requirement code
# for articles in course_requirements.find_all('article'):
#   grade = articles.find('h3')
#   print(grade.string)
#   for paragraph in articles.find('div', class_="course-details").find_all('p'):
#     paragraph_text = paragraph.get_text()
#     sentences = paragraph_text.split('. ')
#     #sentences = list(filter(None, sentences))
#     for central_requirement in sentences:
#       print(central_requirement)
