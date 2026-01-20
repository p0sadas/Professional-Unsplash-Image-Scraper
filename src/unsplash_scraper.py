"""
Unsplash Image Scraper Module.

This module provides the UnsplashScraper class for downloading images from Unsplash.
"""

import logging
import time
from pathlib import Path
from typing import List, Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from . import config


class UnsplashScraper:
    """
    A web scraper for downloading free images from Unsplash.
    
    This class handles browser automation, image URL extraction,
    and downloading images from Unsplash search results.
    
    Attributes:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance for explicit waits
        logger: Logger instance for this class
    """
    
    def __init__(self, headless: bool = False):
        """
        Initialize the Unsplash scraper.
        
        Args:
            headless: If True, run browser in headless mode (no GUI)
        """
        self.logger = self._setup_logger()
        self.driver = self._setup_driver(headless)
        self.wait = WebDriverWait(self.driver, config.WEBDRIVER_TIMEOUT)
        
    def _setup_logger(self) -> logging.Logger:
        """
        Set up logging for the scraper.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(config.LOG_LEVEL)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(config.LOG_FORMAT)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _setup_driver(self, headless: bool) -> webdriver.Chrome:
        """
        Set up and configure the Chrome WebDriver.
        
        Args:
            headless: Whether to run in headless mode
            
        Returns:
            Configured Chrome WebDriver instance
        """
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument(f"user-agent={config.USER_AGENT}")
        
        if headless:
            options.add_argument("--headless")
            
        driver = webdriver.Chrome(options=options)
        
        # Enable DevTools Protocol
        driver.execute_cdp_cmd("Network.enable", {})
        
        # Set extra HTTP headers
        driver.execute_cdp_cmd(
            "Network.setExtraHTTPHeaders",
            {"headers": config.HTTP_HEADERS}
        )
        
        self.logger.info("WebDriver initialized successfully")
        return driver
    
    def scrape_images(self, query: str, num_images: int) -> List[str]:
        """
        Scrape image URLs from Unsplash search results.
        
        Args:
            query: Search query (e.g., "cat", "nature", "technology")
            num_images: Number of images to scrape
            
        Returns:
            List of image URLs
            
        Raises:
            TimeoutException: If page elements don't load in time
        """
        url = config.DEFAULT_SEARCH_URL.format(query=query)
        self.logger.info(f"Starting scrape for query '{query}' - target: {num_images} images")
        
        try:
            # Navigate to search results
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
            
            # Wait for images container to load
            images_container = self.wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, config.SELECTORS["images_container"])
                )
            )
            
            # Get current number of images
            current_count = self._count_current_images(images_container[0])
            self.logger.info(f"Initially loaded {current_count} images")
            
            # Load more images if needed
            if current_count < num_images:
                self._load_more_images(images_container[0], num_images)
            
            # Extract image URLs
            image_urls = self._extract_image_urls(images_container[0])
            
            # Trim to requested number
            if len(image_urls) > num_images:
                image_urls = image_urls[:num_images]
                
            self.logger.info(f"Successfully extracted {len(image_urls)} image URLs")
            return image_urls
            
        except TimeoutException as e:
            self.logger.error(f"Timeout while loading page: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            raise
    
    def _count_current_images(self, container) -> int:
        """
        Count the number of currently loaded images.
        
        Args:
            container: The main images container element
            
        Returns:
            Number of images currently loaded
        """
        columns = container.find_elements(By.XPATH, "./*")
        if not columns:
            return 0
            
        figures = columns[0].find_elements(By.XPATH, "./*")
        # Unsplash uses 3 columns, so multiply by 3
        return len(figures) * 3
    
    def _load_more_images(self, container, target_count: int) -> None:
        """
        Load more images by clicking 'Load More' button and scrolling.
        
        Args:
            container: The main images container element
            target_count: Target number of images to load
        """
        try:
            # Click "Load More" button if it exists
            load_more_btn = self.driver.find_element(
                By.XPATH, 
                config.SELECTORS["load_more_button"]
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", load_more_btn)
            time.sleep(2)
            self.logger.info("Clicked 'Load More' button")
        except NoSuchElementException:
            self.logger.warning("'Load More' button not found, will try scrolling")
        
        # Scroll to load more images
        current_count = self._count_current_images(container)
        
        while current_count < target_count:
            self.driver.execute_script(f"window.scrollBy(0, {config.SCROLL_STEP});")
            time.sleep(config.SCROLL_PAUSE_TIME)
            
            new_count = self._count_current_images(container)
            
            # Break if no new images loaded
            if new_count == current_count:
                self.logger.warning(
                    f"Stopped at {current_count} images - no more available"
                )
                break
                
            current_count = new_count
            self.logger.debug(f"Loaded {current_count} images...")
    
    def _extract_image_urls(self, container) -> List[str]:
        """
        Extract image URLs from the loaded page.
        
        Args:
            container: The main images container element
            
        Returns:
            List of image URLs
        """
        image_urls = []
        columns = container.find_elements(By.XPATH, "./*")
        
        for col_idx, column in enumerate(columns):
            self.logger.debug(f"Processing column {col_idx + 1}/{len(columns)}")
            figures = column.find_elements(By.XPATH, "./*")
            
            for figure in figures:
                try:
                    div_child = figure.find_element(By.XPATH, "./*")
                    
                    # Check if this is an image container
                    if div_child.get_attribute("class") == config.SELECTORS["image_container_class"]:
                        # Navigate through the DOM structure
                        div_child1 = div_child.find_element(By.XPATH, "./*")
                        a_link = div_child1.find_element(By.XPATH, "./*")
                        img = a_link.find_element(By.XPATH, "./*")
                        
                        image_url = img.get_attribute("src")
                        if image_url:
                            image_urls.append(image_url)
                            
                except NoSuchElementException:
                    # Skip elements that don't match expected structure
                    continue
                    
        return image_urls
    
    def download_images(
        self, 
        image_urls: List[str], 
        output_dir: Optional[Path] = None,
        prefix: str = "img"
    ) -> None:
        """
        Download images from URLs to the specified directory.
        
        Args:
            image_urls: List of image URLs to download
            output_dir: Directory to save images (default: config.DOWNLOAD_DIR)
            prefix: Prefix for image filenames (default: "img")
        """
        if output_dir is None:
            output_dir = config.DOWNLOAD_DIR
            
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Downloading {len(image_urls)} images to {output_dir}")
        
        for idx, url in enumerate(image_urls, start=1):
            try:
                # Download image
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                # Generate filename
                filename = config.IMAGE_FILENAME_PATTERN.format(
                    index=idx,
                    extension=config.IMAGE_FORMAT
                )
                filepath = output_dir / filename
                
                # Save image
                with open(filepath, "wb") as f:
                    f.write(response.content)
                    
                self.logger.info(f"Downloaded {idx}/{len(image_urls)}: {filename}")
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to download image {idx}: {e}")
                continue
                
        self.logger.info("Download completed!")
    
    def close(self) -> None:
        """Close the browser and clean up resources."""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures driver is closed."""
        self.close()
