import time
import threading
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver

import Ollama
from Frameworks import Frameworks
from Languages import Languages
from Technologies import Technologies
from charts import create_bar_chart


class Scraper:

    def __init__(self):
        self.languages = Languages.languages
        self.frameworks = Frameworks.frameworks
        self.technologies = Technologies.technologies
        self.radius = ""
        self.location = ""
        self.ai_bool = False
        self.base_url = "https://de.indeed.com/jobs?q=Softwareentwickler&l="
        self.driver = None
        self.wait = None
        self.ollama = None
        self.page_num = 2
        self.stop_event = threading.Event()

    def init_driver(self):
        self.driver = Driver(uc=True, headless=True)
        self.wait = WebDriverWait(self.driver, 10)
        self.ollama = Ollama.Ollama()
        self.driver.get(self.base_url)

    def scrape(self):
        time.sleep(4)
        if self.stop_event.is_set():
            print("Scraping stopped")
            self.driver.quit()
        try:
            self.driver.uc_gui_click_captcha()
        except:
            time.sleep(1)
        time.sleep(3)
        try:
            cookiesDecline = self.driver.find_element(By.XPATH, "//*[text()='Alle ablehnen']")
            cookiesDecline.click()
            print("cookies")
        except:
            time.sleep(1)
        time.sleep(5)
        while self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, f"a[data-testid='pagination-page-{self.page_num}']"))):
            if self.page_num > 2:
                self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, f"a[data-testid='pagination-page-{self.page_num - 1}']")))[0].click()
            time.sleep(2)
            self.page_num += 1
            self.scrape_jobs(self.driver, self.wait, self.ollama, self.ai_bool)

    def scrape_jobs(self, driver, wait, ollama, ai_bool):
        jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='slider_item']")))
        print(len(jobs))
        time.sleep(2)
        for i in range(len(jobs)):
            if self.stop_event.is_set():
                print("Scraping stopped")
                self.driver.quit()
                break
            jobs = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='slider_item']")
            jobs[i].click()
            try:
                job_desc = wait.until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
                print(f"Job {i + 1}:")
                if ai_bool:
                    requirements = ollama.generateAnswer(job_desc)
                else:
                    self.scrape_with_skl(job_desc)
                time.sleep(2)
            except TimeoutException:
                raise Exception("Konnte Beschreibung für Job {i + 1} nicht laden")

    def scrape_with_skl(self, job_desc):
        for language in self.languages:
            if language.lower() in (job_desc.text.lower().split()) or language.lower() in (job_desc.text.lower()):
                self.languages[language] += 1
        for framework in self.frameworks:
            if framework.lower() in (job_desc.text.lower().split()) or framework.lower() in (job_desc.text.lower()):
                self.frameworks[framework] += 1
        for technology in self.technologies:
            if technology.lower() in (job_desc.text.lower().split()) or technology.lower() in (job_desc.text.lower()):
                self.technologies[technology] += 1
        #print(self.languages.items())
        #print(self.frameworks.items())
        #print(self.technologies.items())
        create_bar_chart(self.languages)