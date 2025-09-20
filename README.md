Ubuntu Image Fetcher
A Python tool for mindfully collecting and organizing images from the web. This script is designed to be a simple, respectful, and ethical way to download images, embodying the Ubuntu philosophy of "a person is a person through other persons."

Features
Mindful Downloading: Fetches images by checking HTTP headers first to ensure the content is an image and not a malicious file.

Duplicate Prevention: Prevents re-downloading the same image by checking for file duplicates using a SHA256 hash.

Multiple URL Support: Allows you to download multiple images in a single run by providing a comma-separated list of URLs.

Automatic Organization: Saves all downloaded images to a dedicated Fetched_Images directory.

Getting Started
Prerequisites
To run this script, you need to have Python 3 installed on your system.

Installation
Clone or download this repository to your local machine.

Navigate to the project directory in your terminal.

Install the required requests library:

pip install requests

Usage
Run the script from your terminal:

python ubuntu_image_fetcher.py

When prompted, enter one or more image URLs separated by a comma.

Example:
Please enter image URLs, separated by a comma: (https://www.rottler.com/wp-content/uploads/blow-fly.jpg)

Philosophy
"A person is a person through other persons." - Ubuntu philosophy.

This program connects you to the work of others across the web. We strive to be respectful of the content creators by providing a clean, transparent, and non-intrusive way to collect public images.
