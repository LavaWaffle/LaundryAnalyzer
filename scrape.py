import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

def get_firebase_credentials():
    cred_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')
    if not cred_json:
        print("ERROR")
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY environment variable is not set")
    # try:
    cred_dict = json.loads(cred_json)
    return credentials.Certificate(cred_dict)

# Use the function to get credentials
cred = get_firebase_credentials()
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

# cred = credentials.Certificate('firebase.json')  # Replace with your file path
# firebase_admin.initialize_app(cred)

# Get a Firestore client
# db = firestore.client()

def collection_exists(collection_name):
    try:
        db.collection(collection_name).get()
        return True
    except Exception:
        return False

# Create a new collection (if it doesn't exist)
def create_collection(collection_name):
    if not collection_exists(collection_name):
        db.collection(collection_name).document().set({})  # Create an empty document

def add_data_with_id(collection_name, document_id, data):

    doc_ref = db.collection(collection_name).document(document_id)

    doc_ref.set(data)

    print(f"Data added to document: {doc_ref.id}")


urls = ["https://www.laundryview.com/home/1506/589877048/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/ALLEN,-ROOM-49",
"https://www.laundryview.com/home/1506/589877054/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/BOUSFIELD-RM-101-DRYERS",
"https://www.laundryview.com/home/1506/589877017/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/BOUSFIELD-RM-103-WASHERS",
"https://www.laundryview.com/home/1506/589877019/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/BUSEY-EVANS-ROOM-8",
"https://www.laundryview.com/home/1506/589877004/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/CLARK-HALL,-ROOM-30",
"https://www.laundryview.com/home/1506/589877022/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/DANIELS,-NORTH-ROOM-119",
"https://www.laundryview.com/home/1506/589877043/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/DANIELS,-SOUTH-ROOM-40",
"https://www.laundryview.com/home/1506/589877003/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/FAR,-OGLESBY-ROOM-1",
"https://www.laundryview.com/home/1506/589877021/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/FAR,-TRELEASE-ROOM-13",
"https://www.laundryview.com/home/1506/589877044/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/GOODWIN-GREEN,-GREEN-ROOM-31",
"https://www.laundryview.com/home/1506/589877027/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/GOODWIN-GREEN,-GOODWIN-ROOM-8",
"https://www.laundryview.com/home/1506/589877026/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/HOPKINS,-ROOM-150",
"https://www.laundryview.com/home/1506/589877032/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/ISR,-TOWNSEND-ROOM-80",
"https://www.laundryview.com/home/1506/589877030/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/ISR,-WARDALL-ROOM-12",
"https://www.laundryview.com/home/1506/589877031/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/LAR,-NORTH-ROOM-45",
"https://www.laundryview.com/home/1506/589877038/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/LAR,-SOUTH-ROOM-29",
"https://www.laundryview.com/home/1506/589877057/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/NUGENT,-ROOM-126",
"https://www.laundryview.com/home/1506/589877036/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/NUGENT,-ROOM-31",
"https://www.laundryview.com/home/1506/589877037/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/NUGENT,-ROOM-35",
"https://www.laundryview.com/home/1506/589877040/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/ORCHARD-DOWNS,-NORTH-LAUNDRY",
"https://www.laundryview.com/home/1506/589877041/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/ORCHARD-DOWNS,-SOUTH-LAUNDRY",
"https://www.laundryview.com/home/1506/589877023/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/PAR,-BABCOCK-ROOM-23",
"https://www.laundryview.com/home/1506/589877046/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/PAR,-BLAISDELL-ROOM-21B",
"https://www.laundryview.com/home/1506/589877024/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/PAR,-CARR-ROOM-22",
"https://www.laundryview.com/home/1506/589877008/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/PAR,-SAUNDERS-ROOM-23",
"https://www.laundryview.com/home/1506/589877009/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/SCOTT,-ROOM-170",
"https://www.laundryview.com/home/1506/589877052/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/SHERMAN,-13-STORY-ROOM-52",
"https://www.laundryview.com/home/1506/589877051/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/SHERMAN,-5-STORY--ROOM-29",
"https://www.laundryview.com/home/1506/589877015/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/SNYDER,-ROOM-182",
"https://www.laundryview.com/home/1506/589877002/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/TVD,-TAFT-ROOM-13",
"https://www.laundryview.com/home/1506/589877058/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/TVD,-VAN-DOREN-ROOM-13",
"https://www.laundryview.com/home/1506/589877061/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/WASSAJA,-ROOM-1109",
"https://www.laundryview.com/home/1506/589877028/UNIVERSITY-OF-ILLINOIS-AT-URBANA-CHAMPAIGN/WESTON,-ROOM-100"]

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Check if running in GitHub Actions
    if 'GITHUB_ACTIONS' in os.environ:
        chrome_options.binary_location = "/usr/bin/google-chrome"
    
    return webdriver.Chrome(options=chrome_options)
def scrape_laundry_status(url, driver):
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H-%M-%S')
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    location = url.split('/')[-1]
    print(f"Location: {location}")
    
    divs = soup.find_all('div', class_='list-item ng-scope')
    if (len(divs) == 0):
        pass
        # print("No machines found.")
        # directory = f"./results"
        # Check if the directory exists, if not, create it
        # if not os.path.exists(directory):
            # os.makedirs(directory)

        # with open(f"{directory}/{location}_{formatted_now}.html", "w") as f:
            # f.write(page_source)

    create_collection(location)
    results = []
    for div in divs:
        img = div.find('img')['ng-src']
        key = div.find('span', class_='key ng-binding').text
        status = div.select_one('span.ng-binding.ng-scope')
        status_text = status.text if status else 'N/A'
        
        machine_type = "Washer" if "Washer" in img else "Dryer" if "Dryer" in img else "Unknown"
        print(f"{machine_type}, {key}, {status_text}")
        results.append({'machine_type': machine_type, 'machine_number': key, 'machine_status': status_text})

    if len(results) != 0:
        formatted_now_me = now.strftime('%Y-%m-%d %H:%M:%S')
        washers_only = [x for x in results if x['machine_type'] == 'Washer']
        dryers_only = [x for x in results if x['machine_type'] == 'Dryer']
        others = [x for x in results if x['machine_type'] != 'Washer' and x['machine_type'] != 'Dryer']
        add_data_with_id(location, formatted_now_me, {'washers': washers_only, 'dryers': dryers_only, 'others': others})
    else:
        print("No machines found.")


def main():
    driver = setup_driver()
    try:
        for url in urls:
            scrape_laundry_status(url, driver)
            sleep(2)
            print("---")  # Separator between locations
    finally:
        driver.quit()

if __name__ == "__main__":
    main()