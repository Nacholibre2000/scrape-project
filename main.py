from bs4 import BeautifulSoup
import requests
import csv

# for source.html
with open('source.html', 'r', encoding='utf-8') as file:
  page_content = file.read()

soup = BeautifulSoup(page_content, "html.parser")  # for source.html

# for live url
# url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"

# page = requests.get(url)

#soup = BeautifulSoup(page.text, "html.parser") # for live url

#groundwork
result = soup.find('div', class_="content")
central_contents = result.find('section')
course_requirements = central_contents.find_next_sibling('section')

# Dictionaries to store data
subject_data = {}
grade_data = {}
subsection_data = {}
central_content_data = {}
central_requirement_data = {}

# Keeping track of ids
subject_id = 1
grade_id = 1
subsection_id = 1
central_content_id = 1
central_requirement_id = 1

# List to keep track of original subsections
original_subsections = []
original_sentences = []

# find & id subject_data

#svid12_5dfee44715d35a5cdfa219f
subject_div = soup.find('div', class_="sv-proxy-portlet sv-portlet")
header = subject_div.find('header')
subject_name = header.find('h1')
subject = subject_name.string.strip()

if subject not in subject_data:
  subject_data[subject] = subject_id
  subject_id += 1

# Get current subject ID for use in grade_data
subject_id_current = subject_data[subject]

# for-loop for central content
for idx, central_contents_tags in enumerate(central_contents.find_all(
    'div', class_="course-details"),
                                            start=1):
  grade = central_contents_tags.find('h3').string
  if grade not in grade_data:
    grade_data[grade] = (grade_id, str(subject_id_current)
                         )  # include subject_id_current as foreign key
    grade_id += 1

  grade_id_current, foreign_id_grade = grade_data[grade]

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
        foreign_id_subsection = foreign_id_grade + "-" + str(
          grade_id_current)  # Update the foreign key here
        subsection_data[subsection] = (subsection_id, foreign_id_subsection)
        subsection_id += 1
    else:
      print("No preceding h4 sibling found for ul.")

    subsection_id_current, foreign_id_subsection = subsection_data[subsection]

    for central_content in ul.find_all('li'):
      central_content = central_content.string
      if central_content not in central_content_data:
        foreign_id_content = foreign_id_subsection + "-" + str(
          subsection_id_current)  # Update the foreign key here
        central_content_data[central_content] = (central_content_id,
                                                 foreign_id_content)
        central_content_id += 1

# for-loop for central requirement
for idx, articles in enumerate(course_requirements.find_all('article'), start=1):
    grade = articles.find('h3').string

    if grade == "Kriterier för bedömning av godtagbara kunskaper i slutet av årskurs 3":
        grade = "I årskurs 1–3"

    if grade == "Betygskriterier för slutet av årskurs 6":
        grade = "I årskurs 4–6"

    if grade == "Betygskriterier för slutet av årskurs 9":
        grade = "I årskurs 7–9"

    foreign_id_grade = str(subject_id_current) + "-" + str(grade_id)  # Foreign key is subject ID + grade ID

    if grade not in grade_data:
        grade_data[grade] = (grade_id, foreign_id_grade)  # include foreign_id_grade as foreign key
        grade_id += 1

    grade_id_current, foreign_id_grade = grade_data[grade]

    paragraphs = articles.find('div', class_="course-details").find_all('p')
    for paragraph in paragraphs:
        sentences = paragraph.get_text().split('. ')
        for central_requirement in sentences:
            # append grade if the sentence has been seen before
            if central_requirement in original_sentences:
                central_requirement = central_requirement + "-" + grade
            else:
                original_sentences.append(central_requirement)

            foreign_id_requirement = foreign_id_grade + "-" + str(grade_id_current)  # Foreign key is grade foreign ID + grade ID

            if central_requirement not in central_requirement_data:
                central_requirement_data[central_requirement] = (central_requirement_id, foreign_id_requirement)
                central_requirement_id += 1

# Create and write to CSV files
with open('subject_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "subject"])
  for key, value in subject_data.items():
    writer.writerow([value, key])

with open('grade_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "grade", "foreign_id_subject"])  # add foreign_id_subject
    for key, value in grade_data.items():
        writer.writerow([value[0], key, value[1]])

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
    writer.writerow(["id", "central_requirement", "foreign_id_grades"])
    for key, value in central_requirement_data.items():
        writer.writerow([value[0], key, value[1]])
