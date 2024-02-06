import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

class LoginSuccess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--ignore-ssl-errors=yes')
        firefox_options.add_argument('--ignore-certificate-errors')
        cls.browser = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=firefox_options
        )

    def test_login_flow_with_XSS(self):
        # Langkah 1: Buka halaman utama
        url = os.environ.get('URL')
        self.browser.get(url)
        self.browser.implicitly_wait(5)

        # Langkah 2: Memeriksa halaman utama
        expected_result = "Login"
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

        # Langkah 3: Melakukan login
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "/html/body/form/button").click()
        self.browser.implicitly_wait(10)

        # Langkah 4: Verifikasi login berhasil
        expected_result = "Halo, admin"
        actual_result = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertIn(expected_result, actual_result)

        # Langkah 5: Menuju halaman XSS
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/a[2]").click()
        self.browser.implicitly_wait(5)

        # Langkah 6: Memeriksa halaman XSS
        expected_result = "Dummy Page XSS Detect"
        actual_result = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertIn(expected_result, actual_result)

        # Langkah 7: Menuju halaman untuk mengisi form "thing"
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/a[3]").click()
        self.browser.implicitly_wait(5)

        # Langkah 8: Mengisi form "thing"
        expected_result = "Your thing is coba"
        self.browser.find_element(By.NAME, "thing").send_keys("coba")
        self.browser.find_element(By.NAME, "submit").click()
        self.browser.implicitly_wait(5)

        # Langkah 9: Memeriksa hasil setelah mengisi form "thing"
        rows = self.browser.find_elements(By.CLASS_NAME, "row")
        actual_result = rows[1].text
        self.assertIn(expected_result, actual_result)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
