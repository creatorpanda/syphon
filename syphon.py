import os
import requests
import argparse
from bs4 import BeautifulSoup, Comment

def fetch_comments(url, timeout=5):
    """Fetch HTML comments from web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  #Grab any HTTP error code.
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        
        if comments:
            print(f"Found {len(comments)} comments on {url}")
        else:
            print(f"No comments found on {url}")
        
        return comments
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return str(e)  #Return error message.

def save_comments(content, directory_name, output_file, is_error=False):
    """Save comments or error to file with section headers."""
    with open(output_file, 'a') as f:
        if directory_name:
            f.write(f"----- {directory_name} -----\n")
        
        if is_error:
            #Log error instead of comments.
            f.write(f"Error: {content}\n")
        else:
            for comment in content:
                f.write(f"{comment.strip()}\n")
        
        f.write("\n")

def process_url(base_url, directory, output_file, timeout):
    """Process single URL by fetching comments and saving them."""
    full_url = f"{base_url}/{directory}" if directory else base_url
    result = fetch_comments(full_url, timeout)
    
    if isinstance(result, list) and result:  #Comments found!
        save_comments(result, directory if directory else base_url, output_file)
    elif isinstance(result, str):  #Error encountered!
        save_comments(result, directory if directory else base_url, output_file, is_error=True)

def main():
    parser = argparse.ArgumentParser(description="Syphon: HTML comment harvester.")
    parser.add_argument("url", help="Base URL to scrape for comments.")
    parser.add_argument("-w", "--wordlist", help="Optional wordlist file for directories.")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Set timeout in seconds (default: 5)")
    parser.add_argument("-o", "--output", default="syphonResults.txt", help="Output file to save operation.")
    
    args = parser.parse_args()

    try:
        #Clear output file if exists from previous run.
        if os.path.exists(args.output):
            open(args.output, 'w').close()

        base_url = args.url.rstrip('/')
        
        if args.wordlist:
            #If wordlist provided, iterate over each directory.
            try:
                with open(args.wordlist, 'r') as wl:
                    directories = wl.read().splitlines()
                    for directory in directories:
                        process_url(base_url, directory, args.output, args.timeout)
            except FileNotFoundError:
                print(f"Wordlist file {args.wordlist} not found.")
        else:
            #Only process base URL without any directory.
            process_url(base_url, None, args.output, args.timeout)

    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting gracefully...")

if __name__ == "__main__":
    main()
