import requests
from bs4 import BeautifulSoup

# Fetch the HTML content
url = 'https://secure.rrcu.com/rrcu/uux.aspx#/account/523507?currentTab=transactions&returnTo=_t.navNode.dashboard'
response = requests.get(url)
response.raise_for_status()  # Raise an exception for bad status codes

# Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Extract data (example: find all table rows)
data = []
table_rows = soup.find_all('tr')

for row in table_rows:
    # Extract data from each row (example: find all data cells)
    cells = row.find_all('td')
    # Append the data to a list of lists
    row_data = [cell.text.strip() for cell in cells]  # Convert cells to text and remove whitespace
    data.append(row_data)

# Print the extracted data
print(data)
