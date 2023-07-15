from bs4 import BeautifulSoup
import requests
import csv

# Request webpage
start_url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/kursplaner-for-grundskolan"
response = requests.get(start_url)

# Initialize BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find URLs within specified class
link_div = soup.find('div',
                     class_="sv-proxy-portlet sv-portlet",
                     id="svid12_5dfee44715d35a5cdfa805e")
links = link_div.find_all("p", class_="sv-font-oversiktslankar")

# Extract href from each link and store it in a list
base_url = "https://www.skolverket.se"
urls = [base_url + link.a['href'] for link in links]

# Dictionaries to store data
subject_data = {}
grade_data = {}
subsection_data = {}
central_content_data = {}
central_requirement_data = {}

# Keeping track of ids
school_id = 1
subject_id = 1
grade_id = 1
subsection_id = 1
central_content_id = 1
central_requirement_id = 1

# List to keep track of original subsections
original_subsections = []
original_sentences = []

# Loop through URLs
for url in urls:
  # Get page content
  response = requests.get(url)
  page_content = response.content

  # Initialize BeautifulSoup for the new page
  soup = BeautifulSoup(page_content, "html.parser")

  #groundwork
  result = soup.find('div', class_="content")

  central_contents = result.find('section')
  course_requirements = central_contents.find_next_sibling('section')

  # find & id subject_data

  # find & id subject_data
  subject_div = soup.find('div', class_="sv-proxy-portlet sv-portlet")
  header = subject_div.find('header')
  subject_name = header.find('h1')
  subject = subject_name.string.strip()

  # Always assign a new ID, and increment the counter.
  foreign_id_subject = school_id
  subject_data[subject] = (subject_id, foreign_id_subject)
  subject_id += 1

  # Get current subject ID for use in grade_data
  subject_id_current = subject_data[subject][0]

  # for-loop for central content

  # In the for-loop for central content:
  for idx, central_contents_tags in enumerate(central_contents.find_all(
      'div', class_="course-details"),
                                              start=1):
    grade = central_contents_tags.find('h3').string
    grade += " - " + subject  # Append the subject to the grade to ensure uniqueness

    # Always assign a new ID, and increment the counter.
    foreign_id_grade = str(foreign_id_subject) + "-" + str(subject_id_current)  # Update the foreign key here
    grade_data[grade] = (grade_id, foreign_id_grade)
    grade_id += 1
    grade_id_current, foreign_id_grade = grade_data[grade]

    ul_tags = central_contents_tags.find_all('ul')
    for ul in ul_tags:
      subsection = ul.find_previous_sibling('h4')
      if subsection is None:
        subsection = "Default Subsection"  # replace this with an appropriate default string for your context
      else:
        subsection = subsection.string if subsection.string is not None else "Default Subsection"
  
      subsection += " - " + grade  # Append the grade to the subsection to ensure uniqueness
      foreign_id_subsection = str(foreign_id_grade) + "-" + str(grade_id_current)  # Update the foreign key here
      subsection_data[subsection] = (subsection_id, foreign_id_subsection)
      subsection_id += 1
  
      subsection_id_current, foreign_id_subsection = subsection_data[subsection]

      for central_content in ul.find_all('li'):
        if central_content is None:
          central_content = "Default Central Content"  # replace this with an appropriate default string for your context
        else:
          central_content = central_content.string if central_content.string is not None else "Default Central Content"
        central_content += " - " + subsection  # Append the subsection to the central content to ensure uniqueness
        foreign_id_central_content = str(foreign_id_subsection) + "-" + str(subsection_id_current)  # Update the foreign key here
        central_content_id += 1

        central_content_data[central_content] = (central_content_id, foreign_id_central_content)


  # for-loop for central requirement
  for idx, articles in enumerate(course_requirements.find_all('article'),
                                 start=1):
    grade = articles.find('h3').string
    grade += " - " + subject  # Append the subject to the grade to ensure uniqueness

    # Always assign a new ID, and increment the counter.
    foreign_id_grade = str(foreign_id_subject) + "-" + str(subject_id_current)  # Update the foreign key here
    grade_data[grade] = (grade_id, foreign_id_grade)
    grade_id += 1
    grade_id_current, foreign_id_grade = grade_data[grade]

    paragraphs = articles.find('div', class_="course-details").find_all('p')
    for paragraph in paragraphs:
      sentences = paragraph.get_text().split('. ')
      for central_requirement in sentences:
        central_requirement += " - " + grade
        foreign_id_requirement = str(foreign_id_grade) + "-" + str(grade_id_current)  # Foreign key is grade foreign ID + grade ID

        central_requirement_data[central_requirement] = (central_requirement_id, foreign_id_requirement)
        central_requirement_id += 1
        central_requirement_id_current, foreign_id_requirement = central_requirement_data[central_requirement]

# Create and write to CSV files
with open('subjects_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "subject", "foreign_id_school"])
  for key, value in subject_data.items():
    writer.writerow([value[0], key, value[1]])

with open('grades_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "grade", "foreign_id_subject"])
  for key, value in grade_data.items():
    grade = key.split(" - ")[0].strip()
    writer.writerow([value[0], grade, value[1]])

with open('subsections_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "subsection", "foreign_id_grade"])
  for key, value in subsection_data.items():
    subsection = key.split(" - ")[0].strip()
    writer.writerow([value[0], subsection, value[1]])

with open('central_contents_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "central_content", "foreign_id_subsection"])
  for key, value in central_content_data.items():
    central_content = key.split(" - ")[0].strip()
    writer.writerow([value[0], central_content, value[1]])

with open('central_requirements_data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["id", "central_requirement", "foreign_id_grade"])
  for key, value in central_requirement_data.items():
    central_requirement = key.split(" - ")[0].strip()
    writer.writerow([value[0], central_requirement, value[1]])

