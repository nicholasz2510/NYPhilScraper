import shutil
import requests
import json
from PIL import Image
import os


def scrape(input_url):
    image_links = []
    pages_url = "https://archives.nyphil.org/index.php/booksearch/" + input_url.split("/")[5]
    with requests.Session() as s:
        site = s.get(pages_url)
        to_list = json.loads(site.text)
    for i in to_list:
        image_links.append("https://archives.nyphil.org/index.php/jp2/" + i["location"].replace("/", "|") + "/landscape/1200")
    # return image_links
    for x in range(len(image_links)):
        response = requests.get(image_links[x], stream=True)
        page_num = str(x + 1)
        with open("pages/" + page_num + ".jpg", "wb") as out_file:
            print("Copying page " + page_num + "/" + str(len(image_links)) + "...")
            shutil.copyfileobj(response.raw, out_file)
            print("Done copying page " + page_num)
        del response
    convert_to_pdf(len(image_links))


def convert_to_pdf(num_pages):
    pdf_name = input("\nWhat would you like to name your PDF? ")
    print("Converting to PDF...")
    image_list = []
    for page_num in range(1, num_pages + 1):
        image_list.append(Image.open("pages/" + str(page_num) + ".jpg").convert("RGB"))
        os.remove("pages/" + str(page_num) + ".jpg")
    image_list[0].save("pdfs/" + pdf_name + ".pdf", save_all=True, append_images=image_list[1:])


url = input("What is the URL of the NYPhil archive? ")
print("Scraping...\n")
scrape(url.strip())
print("\nFinished!")
