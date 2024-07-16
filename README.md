
# Website Media Crawler

This script crawls a website starting from a given URL and downloads media files (audio, video, images, GIFs) into categorized folders.

## Disclaimer

This script is intended for use in compliance with all applicable laws and regulations. Users are responsible for ensuring that their use of this script does not violate any laws or ethical guidelines. It is important to obtain proper authorization before crawling and downloading content from any website. The creators of this script are not responsible for any misuse.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `wget` command-line tool
- `ffmpeg` command-line tool (for MKV to MP4 conversion)

## Installation

Install the required Python libraries:

```sh
pip install requests beautifulsoup4
```

Ensure `wget` and `ffmpeg` are installed on your system.

## Usage

```sh
python crawler.py <starting_url> [-o output_folder]
```

- `<starting_url>`: The URL to start crawling from.
- `-o output_folder`: (Optional) The folder to save downloaded media files. Default is `./downloads`.

## Examples

Crawl a website and save media files to the default `./downloads` folder:

```sh
python crawler.py https://example.com
```

Crawl a website and save media files to a specified folder:

```sh
python crawler.py https://example.com -o /path/to/downloads
```

## How It Works

1. The script fetches all HTTP links from the given URL.
2. It recursively crawls the links found on each webpage.
3. It downloads media files (audio, video, images, GIFs) into categorized folders.
4. MKV files are converted to MP4 format using `ffmpeg`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
