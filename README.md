# EDGAR-Scraper

# Challenge:

- Scraper that parses fund holdings pulled from EDGAR, given a ticker or CIK.

# Example:

- For this example, we will use this CIK: 0001166559
- Start on this page: http://www.sec.gov/edgar/searchedgar/companysearch.html
- Enter in the CIK (or ticker), and it will take you here.
- Find the “13F” report documents from the ones listed. Here is a “13F-HR”.
- Parse and generate tab-delimited text from the xml

#Goals:

- Your code should be able to use any mutual fund ticker. Try morningstar.com or lipperweb.com to find valid tickers.
- Be sure to check multiple tickers, since the format of the 13F reports can differ.
- Let us know your thoughts on how to deal with different formats.  
