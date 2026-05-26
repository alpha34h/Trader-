import os, time, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# رابط الـ SSH النفق الخاص بك مع إضافة /stream في آخره
TERMUX_RECEIVER_URL = "https://ea6c57eca2f134.lhr.life/stream" 
TARGET_URL = "https://www.tradingview.com/chart/"

def capture_and_stream():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    img_name = "live_capture.png"
    try:
        driver.get(TARGET_URL)
        time.sleep(5)
        driver.save_screenshot(img_name)
        driver.quit()
        with open(img_name, 'rb') as f:
            requests.post(TERMUX_RECEIVER_URL, files={'image': (img_name, f.read(), 'image/png')})
        if os.path.exists(img_name): os.remove(img_name)
    except Exception as e:
        if driver: driver.quit()
        if os.path.exists(img_name): os.remove(img_name)

if __name__ == '__main__': 
    capture_and_stream()
  
