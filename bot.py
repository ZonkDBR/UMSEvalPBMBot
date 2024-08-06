from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.get("https://auth.ums.ac.id/cas/login?service=https%3A%2F%2Fmyakademik.ums.ac.id%2Faccounts%2Flogin%3Fnext%3D%252F")

username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")

username_field.send_keys("username") # Ganti username menjadi NIM
password_field.send_keys("password") # Ganti dengan password kalian

driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

WebDriverWait(driver, 10).until(
    EC.url_contains("https://myakademik.ums.ac.id/")
)

driver.find_element(By.XPATH, "//a[@href='link/4']").click()

windows_handles = driver.window_handles
driver.switch_to.window(windows_handles[-1])

element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//a[@onclick='getEvalPBM();']"))
)
element.click()

trs = WebDriverWait(driver, 1).until(
    EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@onclick, 'link')]"))
)

for tr_index, tr in enumerate(trs):
    try:
        tr = WebDriverWait(driver, 1). until(
            EC.element_to_be_clickable((By.XPATH, f"(//tr[contains(@onclick, 'link')])[{tr_index + 1}]"))
        )
        tr.click()
        radios = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio'][value='4']")) #Ubah value sesuka kalian, 1 tidak puas sampai 4 sangat puas
        )
        for radio in radios:
            radio.click()
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.pull-right").click()
        try:
            alert = driver.switch_to.alert
            alert.accept()
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "some_element_on_the_page"))
            )
        except:
            pass
    except Exception as e:
        logging.error("Error clicking on tr element: %s", e)

driver.quit()