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

    def test_login_flow(self):
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

        # Langkah 5: Menuju halaman tambah kontak
        expected_result = "Add new contact"
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/a").click()
        self.browser.implicitly_wait(5)
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

        # Langkah 6: Mengisi formulir tambah kontak
        self.browser.find_element(By.ID, "name").send_keys("Fikra")
        self.browser.find_element(By.ID, "email").send_keys("fikra@example.com")
        self.browser.find_element(By.ID, "phone").send_keys("1234567890")
        self.browser.find_element(By.ID, "title").send_keys("Software Engineer")

        # Langkah 7: Menyimpan kontak baru
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.browser.implicitly_wait(5)

        # Langkah 8: Memastikan pengguna kembali ke dashboard setelah menyimpan kontak baru
        expected_result = "Dashboard"
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

        # Langkah 9: Menuju halaman edit kontak
        expected_result = "Change contact"
        self.browser.find_element(By.XPATH, '//*[@id="employee_filter"]/label/input').send_keys("Fikra")
        self.browser.implicitly_wait(5)
        ids = self.browser.find_elements(By.CLASS_NAME, "sorting_1")
        target_id = ids[1].text
        edit_button = self.browser.find_element(By.XPATH, f"//a[@href='update.php?id={target_id}']")
        edit_button.click()
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

        # Langkah 10: Mengupdate kontak
        self.browser.find_element(By.ID, "name").clear()
        self.browser.find_element(By.ID, "name").send_keys("Fikri")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.browser.implicitly_wait(5)

        # Langkah 11: Memastikan pengguna kembali ke dashboard setelah mengupdate kontak
        expected_result = "Dashboard"
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)

        # Langkah 12: Mencari kontak yang telah diupdate
        expected_result = "Fikri"
        self.browser.find_element(By.XPATH, '//*[@id="employee_filter"]/label/input').send_keys("Fikri")
        self.browser.implicitly_wait(3)
        actual_result = self.browser.find_element(By.XPATH, '//*[@id="employee"]/tbody/tr/td[2]').text
        self.assertIn(expected_result, actual_result)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    
if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')