import sys
import os
import streamlit as st


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from ScraperController import ScraperController

if 'controller' not in st.session_state:
    st.session_state.controller = ScraperController()



st.title("Indeed Scraper")
start_scrape_button = st.button("Scrape")
stop_scrape_button = st.button("Stop")
if start_scrape_button:
    st.write("Starting Scraping")
    with st.spinner(text="Scraping in progress...", show_time=True):
        st.session_state.controller.start_scrape()
    st.success("Scraping completed successfully")

if stop_scrape_button:
    st.write("Stopping scraping")
    ret_ans = st.session_state.controller.stop_scrape()
    st.write(ret_ans)