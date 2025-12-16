from ScraperController import ScraperController

def main():
    ScraperController().start_scrape(max_jobs_filter=5, jobs_filtered="pages")

if "__main__":
    main()
