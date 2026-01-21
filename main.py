"""
Unsplash Image Scraper - Main Entry Point

A professional web scraper for downloading free images from Unsplash.
"""

import argparse
import sys
from pathlib import Path

from src.unsplash_scraper import UnsplashScraper


def main():
    """Main function to run the Unsplash scraper."""
    parser = argparse.ArgumentParser(
        description="Download free images from Unsplash",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -q cat -n 10
  python main.py --query "mountain landscape" --num-images 25
  python main.py -q dog -n 15 --headless
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        type=str,
        required=False,
        help="Search query (e.g., 'cat', 'nature', 'technology')"
    )
    
    parser.add_argument(
        "-n", "--num-images",
        type=int,
        required=False,
        help="Number of images to download"
    )
    
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser with GUI (headless is default)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="downloads",
        help="Output directory for images (default: downloads)"
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, use interactive mode
    if not args.query:
        print("=" * 60)
        print("  Unsplash Image Scraper")
        print("=" * 60)
        args.query = input("\nEnter search query (e.g., 'cat', 'nature'): ").strip()
        
        if not args.query:
            print("Error: Search query cannot be empty!")
            sys.exit(1)
    
    if not args.num_images:
        while True:
            try:
                num_str = input("How many images do you want to download? ")
                args.num_images = int(num_str)
                if args.num_images > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
    
    # Create output directory path
    output_dir = Path(args.output)
    
    print(f"\n🔍 Searching for '{args.query}'...")
    print(f"📊 Target: {args.num_images} images")
    print(f"📁 Output: {output_dir.absolute()}\n")
    
    try:
        # Use context manager to ensure driver is closed
        # Headless is default, unless --no-headless flag is used
        headless_mode = not args.no_headless
        with UnsplashScraper(headless=headless_mode) as scraper:
            # Scrape image URLs
            image_urls = scraper.scrape_images(args.query, args.num_images)
            
            if not image_urls:
                print("\n❌ No images found. Try a different search query.")
                sys.exit(1)
            
            print(f"\n✅ Found {len(image_urls)} images")
            
            # Download images
            print(f"\n📥 Downloading images...\n")
            scraper.download_images(image_urls, output_dir)
            
            print(f"\n✨ Successfully downloaded {len(image_urls)} images!")
            print(f"📂 Images saved to: {output_dir.absolute()}")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
