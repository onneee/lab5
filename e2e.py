from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Настройки
LOGIN = "standard_user"
PASSWORD = "secret_sauce"
ITEM_NAME = "Sauce Labs Backpack"

# Запуск браузера
options = Options()
service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

try:
    # 1. Открыть сайт
    driver.get("https://www.saucedemo.com/")

    # 2. Авторизация
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(LOGIN)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    # 3. Найти товар и добавить в корзину
    item = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{ITEM_NAME}']/ancestor::div[@class='inventory_item']//button")))
    item.click()

    # 4. Перейти в корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{ITEM_NAME}']")))

    # 5. Оформить заказ
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "finish").click()

    # 6. Проверка успешной покупки
    confirmation = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    assert confirmation.text == "Thank you for your order!"
    print("Тест успешно пройден: покупка завершена.")

except TimeoutException:
    print("Ошибка: Таймаут ожидания элемента.")

except AssertionError:
    print("Ошибка: Покупка не была завершена корректно.")

finally:
    driver.quit()
