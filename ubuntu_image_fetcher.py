import requests
import os
import hashlib
from urllib.parse import urlparse

def get_file_hash(filepath):
    """Generates a SHA256 hash for a given file to check for duplicates."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def is_duplicate(filepath, known_hashes):
    """Checks if a file is a duplicate based on its hash."""
    file_hash = get_file_hash(filepath)
    if file_hash in known_hashes:
        return True
    known_hashes.add(file_hash)
    return False

def is_safe_to_download(response, safe_mimetypes):
    """
    Checks the Content-Type header to ensure the response is an image.
    This is a basic security precaution against downloading unexpected file types.
    """
    content_type = response.headers.get('Content-Type', '')
    return any(safe_type in content_type for safe_type in safe_mimetypes)

def fetch_image(url, known_hashes, directory="Fetched_Images"):
    """
    Fetches a single image, handles errors, checks for duplicates, and saves it.
    """
    try:
        # Step 1: Check HTTP Headers before downloading content
        # Use a HEAD request to get headers without downloading the full content
        print(f"Checking headers for {url}...")
        head_response = requests.head(url, timeout=10)
        head_response.raise_for_status()

        safe_mimetypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
        if not is_safe_to_download(head_response, safe_mimetypes):
            print(f"✗ File type not supported or unsafe: {head_response.headers.get('Content-Type')}")
            return False

        # Step 2: Download the full image content
        print(f"Fetching full image from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Extract filename from URL or generate a default
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"
        
        filepath = os.path.join(directory, filename)

        # Step 3: Save the image temporarily to check for duplicates
        temp_filepath = filepath + ".tmp"
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)
        
        # Step 4: Check for duplicates before finalizing the save
        if is_duplicate(temp_filepath, known_hashes):
            print(f"✓ Duplicate image found for {filename}. Skipping download.")
            os.remove(temp_filepath)  # Clean up the temporary file
        else:
            os.rename(temp_filepath, filepath) # Rename to final path
            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")
    return False

def main():
    """
    Main function to run the Ubuntu Image Fetcher application.
    """
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get URLs from the user
    urls_input = input("Please enter image URLs, separated by a comma: ")
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    
    if not urls:
        print("No URLs provided. Exiting.")
        return

    # Create directory for saving images
    output_dir = "Fetched_Images"
    os.makedirs(output_dir, exist_ok=True)
    
    known_hashes = set()
    
    print("\nStarting the mindful download process...")
    for url in urls:
        fetch_image(url, known_hashes, output_dir)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()