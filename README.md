#HOW TO 

### To run Locally, do the following (while on root directory): 
```
	python -m SimpleHTTPServer
```

### Important Files:

- index.html is the main file, it includes: 
- js/new.js where the d3 code is. Change stuff here. 
- css/style.css also change stuff here. 

### To scrape fresh data

1. add your fb token to the file in data/scraper2.py 
2. run the following command to scrape and save the data:

```
    python scraper2.py  > newdata.json
```