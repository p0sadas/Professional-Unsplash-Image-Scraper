"""
Configuration module for Unsplash Image Scraper.

This module contains all configurable parameters for the scraper,
including timeouts, file paths, and web driver settings.
"""

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Output directory for downloaded images
DOWNLOAD_DIR = BASE_DIR / "downloads"

# Selenium WebDriver settings
WEBDRIVER_TIMEOUT = 30  # seconds (increased for slow page loads)
SCROLL_PAUSE_TIME = 0.3  # seconds between scrolls
SCROLL_STEP = 300  # pixels to scroll at a time

# User agent string
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121 Safari/537.36"

# HTTP headers
HTTP_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

# Default search URL
DEFAULT_SEARCH_URL = "https://unsplash.com/s/photos/{query}?license=free"

# XPath selectors (can be updated if Unsplash changes their layout)
SELECTORS = {
    "images_container": "div[data-testid='masonry-grid-count-three']",
    "load_more_button": "div[class^='loadMoreButtonContainer-'] button",
    "image_container_class": "container-WSKyvi",
}

# Image file format
IMAGE_FORMAT = "jpg"
IMAGE_FILENAME_PATTERN = "img_{index:04d}.{extension}"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
