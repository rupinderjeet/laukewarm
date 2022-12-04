# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup

from book import read_books


def test_sample():
    with open('sample/books.html') as file:
        content = file.read()

    print(f"read a file with {len(content)} length")

    soup = BeautifulSoup(content, "html.parser")
    read_books(soup)
    # results = soup.find(id="ResultsContainer")

    # # Look for Python jobs
    # print("PYTHON JOBS\n==============================\n")
    # python_jobs = results.find_all(
    #     "h2", string=lambda text: "python" in text.lower()
    # )
    # python_job_elements = [
    #     h2_element.parent.parent.parent for h2_element in python_jobs
    # ]
    #
    # for job_element in python_job_elements:
    #     title_element = job_element.find("h2", class_="title")
    #     company_element = job_element.find("h3", class_="company")
    #     location_element = job_element.find("p", class_="location")
    #     print(title_element.text.strip())
    #     print(company_element.text.strip())
    #     print(location_element.text.strip())
    #     link_url = job_element.find_all("a")[1]["href"]
    #     print(f"Apply here: {link_url}\n")
    #     print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_sample()


