import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def visit_as_admin():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get("http://wormblog:5000/admin")
    time.sleep(1)
    driver.get("http://wormblog:5000/")
    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    while True:
        print("[🤖] AdminBot visiting the blog...")
        try:
            visit_as_admin()
        except Exception as e:
            print(f"[!] AdminBot error: {e}")
        time.sleep(10)
