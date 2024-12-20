from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import base64
from PIL import Image
from io import BytesIO
import time

class WebsiteChecker:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--hide-scrollbars')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def get_full_page_screenshot(self, url):
        try:
            self.driver.get(url)
            
            # Đợi trang load xong
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(("tag name", "body"))
            )
            time.sleep(2)

            # Set viewport cố định
            viewport_width = 1920
            viewport_height = 1080
            self.driver.set_window_size(viewport_width, viewport_height)

            # Lấy chiều cao thực của trang
            total_height = self.driver.execute_script("return Math.max("
                "document.body.scrollHeight, "
                "document.documentElement.scrollHeight);")

            # Scroll xuống cuối trang một lần để load hết
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Scroll lên đầu
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

            # Chụp từng màn hình
            screenshots = []
            current_height = 0

            while current_height < total_height:
                # Chụp viewport hiện tại
                screenshot = self.driver.get_screenshot_as_png()
                
                # Convert và encode base64
                img_base64 = base64.b64encode(screenshot).decode('utf-8')
                screenshots.append(img_base64)

                # Scroll xuống viewport tiếp theo
                current_height += viewport_height
                self.driver.execute_script(f"window.scrollTo(0, {current_height});")
                time.sleep(0.8)

            return {
                'status': 'success',
                'url': url,
                'screenshots': screenshots  # Trả về list các ảnh base64
            }
            
        except Exception as e:
            raise Exception(f"Error capturing website: {str(e)}")

    def check_website(self, url):
        return self.get_full_page_screenshot(url)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()