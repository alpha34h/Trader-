import os, time, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ضع الرابط الخاص بك هنا (الرابط الذي حصلت عليه من تيرموكس + /stream)
TERMUX_RECEIVER_URL = "https://tapes-nearest-divide-cases.trycloudflare.com/stream"
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
            
        if os.path.exists(img_name):
            os.remove(img_name)
            
    except Exception as e:
        print(f"Error: {e}")
        if 'driver' in locals():
            driver.quit()
        if os.path.exists(img_name):
            os.remove(img_name)

if __name__ == '__main__':
    capture_and_stream()
    
