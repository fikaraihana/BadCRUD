import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import random
import string

class CreateContact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=option)
        try:
            cls.url = os.environ['URL']
        except:
            cls.url = "http://localhost"
        cls.name_query = ''.join(random.choices(string.ascii_letters, k=10))
        
    def test(self):
        self.home_check()
        self.login_user()
        self.go_to_logout()
        
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
        self.browser.implicitly_wait(20)
        actual_result = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertIn(expected_result, actual_result)
        
    def go_to_logout(self):
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/a[3]").click()
        self.browser.implicitly_wait(5)
        expected_result = "Login"        
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    
if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')