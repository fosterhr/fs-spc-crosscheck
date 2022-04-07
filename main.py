import os, re
from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

clear = lambda: os.system("cls")

driver_options = Options()
driver_options.add_argument("--log-level=3")
driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=driver_options)

driver.minimize_window()

clear()

def get_fs_courses():
    fs_url = "https://www.fullsail.edu/degrees/cybersecurity-bachelor/courses?fs=campus"
    driver.get(fs_url)

    fs_urls = [url.get_attribute("href") for url in driver.find_elements(by=By.CLASS_NAME, value="schedule-block__row")]
    fs_courses = {}

    print("Building Full Sail University course list...")

    for url in tqdm(fs_urls):
        driver.get(url)

        fs_courses[driver.find_element(by=By.CLASS_NAME, value="header__tertiary").text] = \
            driver.find_element(by=By.CLASS_NAME, value="header__primary").text

    return fs_courses


def get_spc_courses():
    spc_url = "https://web.spcollege.edu/courses/gen-ed"
    driver.get(spc_url)

    spc_rows = driver.find_elements(by=By.CLASS_NAME, value="programCourseDiv")
    spc_courses = {}

    print("Building St. Petersburg College course list (Pt. 1)...")

    for row in tqdm(spc_rows):
        code = row.find_element(by=By.TAG_NAME, value="a").text
        if len(code.split(" ")) > 2: continue
        spc_courses[code] = row.find_element(by=By.CLASS_NAME, value="programCourseTitle").text

    spc_url = "https://www.spcollege.edu/future-students/degrees-training/technology/cybersecurity/cybersecurity-bas-degree"
    driver.get(spc_url)

    spc_rows = driver.find_elements(by=By.CLASS_NAME, value="courserow")

    print("Building St. Petersburg College course list (Pt. 2)...")

    for row in tqdm(spc_rows):
        spc_courses[row.find_element(by=By.TAG_NAME, value="a").get_attribute("innerHTML").replace("&", "").replace("nbsp;", "")] = \
            row.get_attribute("innerHTML").split(">")[4].split("<")[0].strip().replace("amp;", "")

    return spc_courses

fs = get_fs_courses()
spc = get_spc_courses()

matches = {}

print("Cross-checking course lists...")
for fs_course in tqdm(fs):
    if fs_course in spc:
        matches[fs_course] = fs[fs_course]

print("")
print(f"Found {len(matches)} matches.")
