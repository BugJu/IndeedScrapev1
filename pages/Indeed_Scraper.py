import sys
import os
import streamlit as st

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from ScraperController import ScraperController

if 'controller' not in st.session_state:
    st.session_state.controller = ScraperController()

st.title("Indeed Scraper")
choice_max = st.selectbox("Pick to scrape after max Jobs or max Pages",
                          ("Jobs", "Pages"), index=1, placeholder="Select method...")
max_pages = st.slider("Select max. pages to Scrape", 1, 20, 5, disabled=True if choice_max == "Jobs" else False)
max_jobs = st.slider("Select max. jobs to Scrape", 1, 100, 10, disabled=True if choice_max == "Pages" else False)

start_scrape_button = st.button("Scrape")
stop_scrape_button = st.button("Stop")
if start_scrape_button:
    st.write("Starting Scraping")
    with st.spinner(text="preparing Scrape...", show_time=True):
        if choice_max == "Jobs":
            st.session_state.controller.start_scrape(max_filter=max_jobs, jobs_filtered="Jobs")
        else:
            st.session_state.controller.start_scrape(max_filter=max_pages, jobs_filtered="Pages")
    st.success("Scraping started")

if stop_scrape_button:
    st.write("Stopping scraping")
    ret_ans = st.session_state.controller.stop_scrape()
    st.write(ret_ans)

