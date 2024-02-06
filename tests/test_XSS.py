import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

class XSSButton(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--ignore-ssl-errors=yes')
        firefox_options.add_argument('--ignore-certificate-errors')
        cls.browser = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=firefox_options
    )
        
    def test(self):
        self.home_check()
        self.login_user()
        self.go_to_XSS()
        self.type_thing()
        
    def home_check(self):
        url = os.environ.get('URL')
        self.browser.get(url)
        self.browser.implicitly_wait(5)
        expected_result = "Login"        
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)
        
    def login_user(self):
        expected_result = "Halo, admin"
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "/html/body/form/button").click()
        self.browser.implicitly_wait(5)
        actual_result = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertIn(expected_result, actual_result)
        
    def go_to_XSS(self):
        expected_result = "Dummy Page XSS Detect"
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/a[2]").click()
        self.browser.implicitly_wait(5)
        actual_result = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertIn(expected_result, actual_result)
        
    def type_thing(self):
        expected_result = "Your thing is coba"
        self.browser.find_element(By.NAME, "thing").send_keys("coba")
        self.browser.find_element(By.NAME, "submit").click()
        self.browser.implicitly_wait(5)
        rows = self.browser.find_elements(By.CLASS_NAME, "row")
        actual_result = rows[1].text
        self.assertIn(expected_result, actual_result)
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    
if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')