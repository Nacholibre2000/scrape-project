from bs4 import BeautifulSoup
import requests

url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
#subsection = soup.find_all('h4', class_="c12638") # to find subsection

central_content = soup.find_all('section', class_="courses-wrapper")

for ul in central_content:
  subsection, central_content = 
  print(subsection.ul)
  print(central_content.li)

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
