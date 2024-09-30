# Syphon: HTML Comment Harvester

Syphon is a Python-based tool designed to harvest HTML comments from web pages.\
It allows users to scrape comments from multiple pages, organize them into sections, and log them into a text file.

## Features
- Scrapes HTML comments from any website.
- Supports wordlists for directory traversal.
- Supports custom request timeout.
- Logs server errors (f.e., 403 and 404).
- Exports results.

## Dependencies
- beautifulsoup4

## Examples

### Simple URL Scan
*http/https protocol is required.*
```
python3 syphon.py https://example.com
```
or
```
python3 syphon.py https://example.com/specificdir
```

### Scan with Wordlist
**Syphon Wordlist scans**:
- *ignore absolute paths. only the domain will be used, following the wordlist's directories.*
- *operate only on indicated directories. To include the homepage, leave a blank line in the wordlist.*
```
python3 syphon.py https://example.com -w selectedWordlist.txt
```

### Scan with custom Timeout
*if not specified, the default timeout value is 5 seconds*
```
python3 syphon.py https://example.com -t 7
```

### Scan with custom Output file
*If not specified, Syphon will create a default output file, named "syphonResults.txt", at the location it was run.*
```
python3 syphon.py https://example.com -o specificName.txt
```

### Scan using all parameters
```
python3 syphon.py https://example.com -w selectedWordlist.txt -t 10 -o specificName.txt
```
