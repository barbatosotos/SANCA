# sheet id = xxxxxxxxxxxxxxxxx
import requests
from bs4 import BeautifulSoup
import re
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to replace href attribute values with a custom URL using regular expressions
def replace_href_with_custom_url(content, custom_url):
    pattern = r'href="([^"]*)"'
    replaced_content = re.sub(pattern, f'href="{custom_url}"', content)
    return replaced_content

# menambah class di tag <blockquote>
def add_blockquote_class(content, kastemklas):
    pattern = r'<blockquote\s*>'
    replaced_content = re.sub(pattern, f'{kastemklas}', content)
    return replaced_content

# Prompt for the list of URLs to extract text from
urls_prompt = "Masukkan URL situs web yang ingin Anda ekstrak teksnya? Berikan URL, dipisahkan dengan koma.\n"

# Get input from the user
urls = [url.strip() for url in input(urls_prompt).split(",")]

# Set up Google Sheets API settings
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Open the spreadsheet
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxxxxxxxxxxxx'
worksheet_index = 0  # Index of the worksheet to write to
spreadsheet = gc.open_by_url(spreadsheet_url)
worksheet = spreadsheet.get_worksheet(worksheet_index)

# Loop through each URL
for i, url in enumerate(urls):
    # Get the title from the URL
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip()

    # Combine the extraction results from HTML elements
    extracted_data = []

    for element in soup.find_all(["h2", "h3", "p", "div", "blockquote"], class_=["mbr-section-title", "mbr-section-subtitle", "mbr-text"]):
        kastemklas = "<blockquote class='arab'>"
        # if element.name == "blockquote":
            # element_html = [add_blockquote_class(text, kastemklas) for text in extracted_data]
            # extracted_data.append(element_html)
        # else:
        extracted_data.append(str(element))
    extracted_data = [add_blockquote_class(text, kastemklas) for text in extracted_data]
    # Replace href attribute values with a custom URL
    custom_url = "https://nyagaklangit.blogspot.com"  # Replace with your custom URL
    extracted_data = [replace_href_with_custom_url(text, custom_url) for text in extracted_data]

    # Combine the extraction results into HTML text
    html_content = ''.join(extracted_data)

    # Save the extraction results as an HTML file
    file_name = f"output_{i+1}.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>" + title + "</title>\n</head>\n<body>\n")
        file.write(html_content)
        file.write("\n</body>\n</html>")

    # Send the extraction results to Google Sheets
    cell_range = f"A{i+1}:A{i+1}"  # Cell range in column A to store the HTML text
    worksheet.update(cell_range, [[html_content]])

    print(f"Data dari URL {url} telah ditulis ke spreadsheet dan disimpan sebagai file HTML (output_{i+1}.html).")
