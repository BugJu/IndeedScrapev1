import time
import threading

import pandas as pd
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
import streamlit as st
import altair as alt
from string import punctuation

import Ollama
from Frameworks import Frameworks
from Languages import Languages
from Technologies import Technologies




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
        self.job_count = 0
        self.max_pages = 5
        self.max_jobs = 10
        self.jobs_bool = False
        self.ended = False

    def init_driver(self):
        self.driver = Driver(uc=True, headless=True)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()
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
        print(self.max_jobs)
        print(self.max_pages)
        while self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, f"a[data-testid='pagination-page-{self.page_num}']"))) and not self.ended:
            if not self.jobs_bool:
                if self.page_num - 1 > self.max_pages:
                    print("stopped because max pages are reached")
                    print("heier")
                    break
            else:
                if self.job_count > self.max_jobs:
                    print("stopped because max jobs are reached")
                    print("heier #2")
                    break
            if self.page_num > 2:
                self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, f"a[data-testid='pagination-page-{self.page_num - 1}']")))[0].click()
            time.sleep(2)
            self.page_num += 1
            self.scrape_jobs(self.driver, self.wait, self.ollama, self.ai_bool)
        self.driver.quit()
        return self.languages

    def scrape_jobs(self, driver, wait, ollama, ai_bool):
        chart_placeholder = st.empty()
        progress = st.progress(0)
        status = st.empty()
        jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='slider_item']")))
        print(len(jobs))
        time.sleep(2)
        for i in range(len(jobs)):
            self.job_count += 1
            if self.jobs_bool:
                if self.job_count > self.max_jobs:
                    print("stopped because max pages are reached")
                    print("heier #3")
                    self.driver.quit()
                    self.ended = True
                    return self.languages
            if self.stop_event.is_set():
                print("Scraping stopped")
                self.driver.quit()
                self.ended = True
                break
            jobs = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='slider_item']")
            jobs_i = wait.until(EC.element_to_be_clickable(jobs[i]))
            jobs_i.click()
            try:
                job_desc = wait.until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
                print(f"Job {i + 1}:")
                if ai_bool:
                    ollama.generateAnswer(job_desc)
                else:
                    self.scrape_with_skl(job_desc)
                time.sleep(2)

            except TimeoutException:
                raise Exception("Konnte Beschreibung für Job {i + 1} nicht laden")
        return self.languages

    def scrape_with_skl(self, job_desc):
        job_desc = job_desc.text.lower()
        for char in punctuation:
            if char in [" ", "#"]:  # Hier ignorieren wir Leerzeichen und #
                continue
            job_desc = job_desc.replace(char, " ")
        for language in self.languages:
            if language.lower() in (job_desc.split()):
                self.languages[language] += 1
        for framework in self.frameworks:
            if framework.lower() in (job_desc.split()):
                self.frameworks[framework] += 1
        for technology in self.technologies:
            if technology.lower() in (job_desc.split()):
                self.technologies[technology] += 1
        # print(self.languages.items())
        # print(self.frameworks.items())
        # print(self.technologies.items())

    def create_bar_chart(self, data_dict, chart_placeholder):
        # Daten vorbereiten
        sorted_dict = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
        df = pd.DataFrame(list(sorted_dict.items()), columns=['languages', 'count'])
        df = df[df['count'] > 0].reset_index(drop=True)
        df['count'] = df['count'].astype(float)

        # Altair-Chart mit expliziten Datentypen
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('languages:N', sort=alt.EncodingSortField(field='count', order='descending')),
            # Sortierung nach count
            y=alt.Y('count:Q')  # Expliziter quantitativer Typ
        )

        with chart_placeholder:
            st.altair_chart(chart, use_container_width=True)
