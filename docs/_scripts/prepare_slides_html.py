import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--html_file",
    type=str,
    action="store",
    required=True,
    help="'file:///' path to the html file you want to prepare. Opening the local html file in your browser should give you a valid one.",
)

args = parser.parse_args()

print(args.html_file)

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(args.html_file)
slides_html = driver.find_element_by_tag_name("body")
stats_for_nerds_html = slides_html.get_attribute("innerHTML")

with open("prepared_stats_for_nerds.slides.html", "w") as slides_file:
    slides_file.write(stats_for_nerds_html)

driver.close()
