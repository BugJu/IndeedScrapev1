from selenium import webdriver
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver

import Ollama


def main():
    #location = input("Please enter location to Scrape or blank for whole Germany: ")
    #radius = input("Please enter radius to Scrape or blank for 35 default: ")

    #if location != "":
    #    base_url = "https://de.indeed.com/jobs?q=Softwareentwickler&l="+location+"&radius="+radius
    #else:
    #    base_url = "https://de.indeed.com/jobs?q=Softwareentwickler&l="
    base_url = "https://de.indeed.com/jobs?q=Softwareentwickler&l="
    driver = Driver(uc=True, headless=False)
    wait = WebDriverWait(driver, 10)
    ollama = Ollama.Ollama()

    driver.get(base_url)
    try:
        driver.uc_gui_click_captcha()
    except:
        time.sleep(1)
    cookiesDecline = driver.find_element(By.XPATH,"//*[text()='Alle ablehnen']")
    cookiesDecline.click()
    jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='slider_item']")))

    print(len(jobs))
    for i in range(len(jobs)):

        jobs = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='slider_item']")
        jobs[i].click()
        try:
            job_desc = wait.until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
            print(f"Job {i + 1}:")
            requirements = ollama.generateAnswer(job_desc.text)
            print(requirements)
            time.sleep(2)
        except TimeoutException:
            raise Exception ("Konnte Beschreibung für Job {i + 1} nicht laden")

    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    main()
