from bs4 import BeautifulSoup
import requests

url = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet?url=-996270488%2Fcompulsorycw%2Fjsp%2Fsubject.htm%3FsubjectCode%3DGRGRSAM01%26tos%3Dgr&sv.url=12.5dfee44715d35a5cdfa219f"

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
coursedetails = soup.find_all("div", {"class": "course-details"})

print(coursedetails)
#print(soup)
