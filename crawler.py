import os
import requests
from bs4 import BeautifulSoup
import subprocess
from urllib.parse import urljoin, urlparse
import argparse

def fetch_links(url):
    """
    Fetch all the HTTP links from a given URL.
    
    Args:
        url (str): The URL to fetch links from.

    Returns:
        list: A list of absolute URLs found on the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
        return links
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return []

def download_media(url, output_folder):
    """
    Download media files from a given URL into categorized folders.

    Args:
        url (str): The URL of the media file.
        output_folder (str): The base folder to save downloaded media files.
    """
    media_types = {
        "Audio": ["mp3"],
        "Video": ["mp4", "mkv"],
        "Images": ["jpg", "jpeg", "png", "webp", "svg"],
        "GIFs": ["gif"]
    }

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if filename:
        file_ext = filename.split('.')[-1].lower()
        for folder, extensions in media_types.items():
            if file_ext in extensions:
                folder_path = os.path.join(output_folder, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, filename)
                if not os.path.exists(file_path):
                    wget_command = f"wget -P {folder_path} -A {file_ext} -nd -e robots=off --wait=1 --random-wait --adjust-extension --convert-links --span-hosts --no-parent {url}"
                    subprocess.run(wget_command, shell=True)
                    if file_ext == "mkv":
                        convert_to_mp4(file_path)

def convert_to_mp4(file_path):
    """
    Convert MKV video files to MP4 format.

    Args:
        file_path (str): The path to the MKV file.
    """
    output_path = file_path.rsplit('.', 1)[0] + '.mp4'
    ffmpeg_command = f"ffmpeg -i {file_path} -codec copy {output_path}"
    subprocess.run(ffmpeg_command, shell=True)
    os.remove(file_path)

def crawl(url, output_folder):
    """
    Recursively crawl a website and download media files.

    Args:
        url (str): The starting URL for crawling.
        output_folder (str): The base folder to save downloaded media files.
    """
    if url not in visited:
        visited.add(url)
        links = fetch_links(url)
        for link in links:
            crawl(link, output_folder)
        download_media(url, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl a website and download media files.")
    parser.add_argument('url', type=str, help='The starting URL for crawling')
    parser.add_argument('-o', '--output', type=str, default='./downloads', help='The output folder for downloaded files')
    args = parser.parse_args()

    start_url = args.url
    output_folder = args.output
    visited = set()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    crawl(start_url, output_folder)
