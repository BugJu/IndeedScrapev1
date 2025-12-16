import threading

from Scraper import Scraper


class ScraperController:
    def __init__(self):
        self.scraper = Scraper()
        self.scraper_thread = None
        self.stop_event = threading.Event()

    def start_scrape(self, max_jobs_filter, jobs_filtered):
        if self.scraper_thread and self.scraper_thread.is_alive():
            print("Scraping läuft bereits")
            return

        self.scraper.jobs_bool = jobs_filtered == "Jobs"
        self.scraper.max_jobs = max_jobs_filter
        self.scraper.max_pages = max_jobs_filter
        self.stop_event.clear()
        self.scraper.stop_event = self.stop_event
        self.scraper.init_driver()
        self.scraper_thread = threading.Thread(target=self.scraper.scrape)
        self.scraper_thread.start()

    def stop_scrape(self):
        if not self.scraper_thread or not self.scraper_thread.is_alive():
            return ("Kein aktiver Scraping-Prozess")

        self.scraper.stop_event.set()
        print("Scraping stopped")
        self.scraper_thread.join()
        self.scraper_thread.join(timeout=10)

        if self.scraper_thread.is_alive():
            print("Scraping-Prozess konnte nicht normal beendet werden")
        self.scraper_thread = None
        return None
