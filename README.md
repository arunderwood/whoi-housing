# whoi-housing

WHOI has a _Community Housing_ page where renters can find suitable housing.  However the data on the page has some minor usability issues and I wanted an excuse to do a web scraping project. 

## Running

The following will perform a scrape and output the results as JSON.
```bash
scrapy crawl --nolog -o - -t json whoi
```