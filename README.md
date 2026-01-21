<div align="center">

![Banner](banner.png)

# 🖼️ Unsplash Image Scraper

### Download free high-quality images from Unsplash with ease

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.16%2B-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

[English](#english) • [Español](#español)

</div>

---

## English

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## ✨ Features

- 🔍 **Smart Search** - Search for any topic and download related images
- 🚀 **Automated Scrolling** - Automatically loads more images to meet your requirements
- 📦 **Batch Download** - Download multiple images in one go
- ⚙️ **Configurable** - Easy to customize settings and parameters
- 🎯 **CLI Support** - Both command-line and interactive modes
- 📝 **Comprehensive Logging** - Track the scraping process with detailed logs
- 🧹 **Clean Code** - Well-structured, documented, and following PEP 8 standards
- 🔒 **Error Handling** - Robust error handling for network issues and timeouts
- 🎨 **Free License Only** - Only downloads images with free licenses from Unsplash

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **Google Chrome Browser** (latest version recommended)
- **ChromeDriver** - Will be automatically managed by Selenium

> **Note:** This scraper uses Selenium WebDriver which will automatically download and manage ChromeDriver for you.

## 📥 Installation

1. **Clone the repository**

```bash
git clone https://github.com/p0sadas/unsplash-image-scraper.git
cd unsplash-image-scraper
```

2. **Create a virtual environment** (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Interactive Mode

Simply run the main script without arguments:

```bash
python main.py
```

You'll be prompted to enter:

- Search query (e.g., "mountains", "technology", "animals")
- Number of images to download

### Command-Line Mode

```bash
# Basic usage (runs in headless mode by default)
python main.py -q "cats" -n 10

# With custom output directory
python main.py -q "nature" -n 25 -o "my_images"

# Show browser window (disable headless mode)
python main.py -q "technology" -n 15 --no-headless
```

### Available Arguments

| Argument        | Short | Description                               | Required |
| --------------- | ----- | ----------------------------------------- | -------- |
| `--query`       | `-q`  | Search query (e.g., 'cat', 'nature')      | No\*     |
| `--num-images`  | `-n`  | Number of images to download              | No\*     |
| `--output`      | `-o`  | Output directory (default: downloads)     | No       |
| `--no-headless` | -     | Show browser window (headless is default) | No       |
| `--help`        | `-h`  | Show help message                         | No       |

\*If not provided, interactive mode will be used.

## ⚙️ Configuration

You can customize the scraper behavior by modifying `src/config.py`:

```python
# Timeouts
WEBDRIVER_TIMEOUT = 20  # seconds
SCROLL_PAUSE_TIME = 0.3  # seconds between scrolls

# Output
DOWNLOAD_DIR = BASE_DIR / "downloads"
IMAGE_FORMAT = "jpg"

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
```

## 📁 Project Structure

```
unsplash-image-scraper/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration settings
│   └── unsplash_scraper.py   # Main scraper class
├── downloads/                # Downloaded images (created automatically)
├── main.py                   # Entry point script
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md               # This file
```

## 💡 Examples

### Example 1: Download Cat Images

```bash
python main.py -q "cats" -n 20
```

Output:

```
🔍 Searching for 'cats'...
📊 Target: 20 images
📁 Output: C:\path\to\downloads

✅ Found 20 images
📥 Downloading images...

✨ Successfully downloaded 20 images!
📂 Images saved to: C:\path\to\downloads
```

### Example 2: Using as a Python Module

```python
from src.unsplash_scraper import UnsplashScraper
from pathlib import Path

# Create scraper instance
with UnsplashScraper(headless=True) as scraper:
    # Scrape image URLs
    urls = scraper.scrape_images("mountains", num_images=10)

    # Download images
    output = Path("my_mountains")
    scraper.download_images(urls, output_dir=output)

print(f"Downloaded {len(urls)} images!")
```

### Example 3: Run with Browser Visible

```bash
# Show the browser window (useful for debugging)
python main.py -q "abstract art" -n 30 --no-headless
```

## 🔍 Troubleshooting

### Issue: "ChromeDriver not found"

**Solution:** Selenium 4.16+ automatically manages ChromeDriver. Ensure you have the latest version:

```bash
pip install --upgrade selenium
```

### Issue: "TimeoutException"

**Solution:** This usually means the page took too long to load. Try:

- Increasing `WEBDRIVER_TIMEOUT` in `src/config.py`
- Checking your internet connection
- Ensuring Unsplash is accessible in your region

### Issue: "No images found"

**Solution:**

- Try a different search query
- Ensure you're searching for topics that exist on Unsplash
- Check if Unsplash has changed their page structure (XPath selectors may need updating)

### Issue: "Download fails for some images"

**Solution:** This is normal - some images may be temporarily unavailable. The scraper will log errors and continue with other images.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate documentation.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect Unsplash's [Terms of Service](https://unsplash.com/terms) and [API Guidelines](https://unsplash.com/api-terms). Always give credit to photographers when using their images.

## 🙏 Acknowledgments

- [Unsplash](https://unsplash.com/) for providing free high-quality images
- [Selenium](https://www.selenium.dev/) for web automation capabilities
- The open-source community for inspiration and support

---

<div align="center">

Made with ❤️ by Angel Posadas

⭐ Star this repo if you found it helpful!

</div>
