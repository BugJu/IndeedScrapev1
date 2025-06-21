# IndeedScrapev1

A web scraper for Indeed job listings that extracts programming languages and frameworks required in job descriptions using AI.

## Description

IndeedScrapev1 is a tool that automates the process of scraping job listings from Indeed's German website, specifically targeting software development positions. It uses Selenium for web scraping and the Ollama API with the Mistral language model to analyze job descriptions and extract the programming languages required for each position.

## Features

- Scrapes job listings from Indeed's German website
- Automatically handles cookies and CAPTCHA challenges
- Extracts job descriptions from each listing
- Uses AI (Mistral model via Ollama) to identify programming languages required in job descriptions
- Formats the output as a clean list of programming languages

## Prerequisites

- Python 3.x
- Ollama running locally with the Mistral model
- Chrome browser

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/IndeedScrapev1.git
   cd IndeedScrapev1
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install selenium seleniumbase requests
   ```

4. Install and run Ollama with the Mistral model:
   ```
   # Follow instructions at https://ollama.ai/ to install Ollama
   ollama pull mistral
   ollama run mistral
   ```

## Usage

1. Make sure Ollama is running with the Mistral model on localhost:11434
2. Run the scraper:
   ```
   python Scraper.py
   ```

3. The script will:
   - Open Indeed's German website
   - Handle cookies and CAPTCHA
   - Scrape job listings for "Softwareentwickler"
   - Extract and analyze job descriptions
   - Print the programming languages required for each job

## Project Structure

- `Scraper.py`: Main script that handles web scraping using Selenium
- `Ollama.py`: Handles communication with the Ollama API to extract programming languages from job descriptions
- `Languages.py`: Contains enumerations of programming languages and frameworks for standardization

## Dependencies

- selenium: For browser automation and web scraping
- seleniumbase: Enhanced Selenium framework with additional features
- requests: For making HTTP requests to the Ollama API

## Notes

- The scraper is currently configured to search for "Softwareentwickler" (Software Developer) positions in Germany
- You can modify the search parameters in the `main()` function of `Scraper.py`
- The Ollama service must be running locally on port 11434