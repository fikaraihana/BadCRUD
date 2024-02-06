import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

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
        
    def test_1_home_check(self):
        self.browser.get('http://127.0.0.1:81/login.php')
        expected_result = "Login"        
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)
        
    def test_2_login_user(self):
        expected_result = "Halo, admin"
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "/html/body/form/button").click()
        actual_result = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertIn(expected_result, actual_result)
        
    def test_3_go_to_create_contact(self):
        expected_result = "Add new contact"
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/a").click()
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)
        
    def test_4_create_contact(self):
        # Isi formulir dengan data kontak baru
        self.browser.find_element(By.ID, "name").send_keys("Fikra")
        self.browser.find_element(By.ID, "email").send_keys("fikra@example.com")
        self.browser.find_element(By.ID, "phone").send_keys("1234567890")
        self.browser.find_element(By.ID, "title").send_keys("Software Engineer")

        # Simpan data kontak baru
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Tunggu beberapa detik untuk memastikan data disimpan
        self.browser.implicitly_wait(2)

        # Verifikasi apakah pengguna diarahkan kembali ke halaman index.php setelah menambahkan kontak baru
        expected_result_after_save = "Dashboard"
        actual_result_after_save = self.browser.title
        self.assertIn(expected_result_after_save, actual_result_after_save)
                
    def test_5_go_to_edit_contact(self):
        expected_result = "Change contact"
        self.browser.find_element(By.XPATH, '//*[@id="employee_filter"]/label/input').send_keys("Fikra")
        ids = self.browser.find_elements(By.CLASS_NAME, "sorting_1")
        target_id = ids[1].text
        edit_button = self.browser.find_element(By.XPATH, f"//a[@href='update.php?id={target_id}']")
        edit_button.click()
        
        actual_result = self.browser.title
        self.assertIn(expected_result, actual_result)
        
    def test_6_Update_contact(self):
        # Isi formulir dengan data kontak baru
        self.browser.find_element(By.ID, "name").clear()
        self.browser.find_element(By.ID, "name").send_keys("Fikri")

        # Simpan data kontak baru
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Tunggu beberapa detik untuk memastikan data disimpan
        self.browser.implicitly_wait(2)

        # Verifikasi apakah pengguna diarahkan kembali ke halaman index.php setelah menambahkan kontak baru
        expected_result_after_save = "Dashboard"
        actual_result_after_save = self.browser.title
        self.assertIn(expected_result_after_save, actual_result_after_save)
        
    def test_7_find_edited_contact(self):
        expected_result = "Fikri"
        self.browser.find_element(By.XPATH, '//*[@id="employee_filter"]/label/input').send_keys("Fikri")
        actual_result = self.browser.find_element(By.XPATH, '//*[@id="employee"]/tbody/tr/td[2]').text
        self.assertIn(expected_result, actual_result)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    
if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')