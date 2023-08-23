# Portfolio Finder

This application scans for user pages on a domain. Created for finding  student portfolio pages on a Google Sites domain.

## Overview

The scanner works by generating random first and last name combinations, appending "portfolio" and trying them as page URLs on the target domain. Any 200 responses are logged as potential portfolio pages.

The scanner uses a configurable number of threads to send requests in parallel for faster scanning. Pages already tried are tracked in a text file to avoid duplicates.

## Usage
Running `scanner.py` will start scanning using the configured settings. All pages will be appended to `tried_pages.txt` and found pages will be appended to `found_pages.txt`.

### Configuration

The `config.json` file contains the following settings:

- `base_url` - The base URL of the site to scan, e.g. https://www.example.com
- `cookies` - Session coocies required for authentication to access to user pages
- `batch_size` - Number of random pages to try per batch
- `threads` - Number of concurrent requests to make
- `log_level` - Logging level 
  - 0 - None
  - 1 - Found pages
  - 2 - Found pages + stats
  - 3 - Found pages + stats + progress bars


#### Example `config.json`
```json
{
    "batch_size":500,
    "threads":25,

    "log_level": 1,

    "base_url": "https://sites.google.com/<school_domain>",
    "cookies":
    {
        "cookie_1": "cookie_1",
        "cookie_2": "cookie_2"
    }
}
```

### Names
The `first_names.txt` and `last_names.txt` files should be populated with first and last names, separated by new lines, to use for generating page names.




## Requirements
- Python 3.6+
- `requests` (install with pip)
- `concurrent.futures` (install with pip)
- `progress_bar` custom module (already in repository)
- `config.json` (see [Configuration](#configuration))
- `first_names.txt` (see [Names](#names))
- `last_names.txt` (see [Names](#names))


## Implementation

### The main logic is in `scanner.py`.

- `check_page()` checks if a page exists using a GET request and logs it if found

- `generate_name()` combines random first and last names

- `get_pages_to_try()` generates a batch of random names using `generate_name()` while avoiding duplicates

- `scan_pages()` runs checks concurrently across threads

- `progress_bar` handles scanning status display



## Possible Use Cases and Applications
- Teacher could use it to easily find and review student portfolios on a class website

- School administrator could use it to audit student portfolios and ensure they meet standards

- The IT department could use it to generate a list of all student pages for monitoring and auditing

- Academic researchers could use it to analyze differences in portfolios across demographics, years, etc.

- It could be integrated into a student portfolio platform to automatically index and display profiles

## Notes

- Designed as proof of concept demonstrating website scraping techniques

- Not intended for unauthorized access - use on sites you have permission for
  
- Can be adapted to other similar scraping tasks by updating page generation logic
