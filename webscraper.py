import requests
import pandas as pd
import os

# function that returns a dictionary of bank names and their corresponding excel file urls
def get_excel_urls(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(base_url, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve content from {base_url}: {e}")
        return
    if response.status_code == 200:
        # using pandas to try and get the table, then parsing the bank names and links
        table = pd.read_html(response.content,extract_links="all")[0]
        table.drop(table.index[-1],inplace=True)
        bank_names = [cell[0] for cell in table.iloc[:,0].values]
        links = [cell[1] for cell in table.iloc[:,1].values]
        links = ['https://nbs.rs/static/nbs_site/gen' + str(link[8:]) for link in links]
        return dict(zip(bank_names, links))
    else:
        print(f"Failed to retrieve content from {base_url}")

def download_file(url, download_path):
    local_filename = url.split('/')[-1]
    local_filepath = os.path.join(download_path, local_filename)


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve content from {url}: {e}")
        return
    if response.status_code == 200:
        os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
        with open(local_filepath, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to retrieve content from {url}")

    print(f"Downloaded: {local_filename}")
