## The folder structure is quite self explanatory:
- The crawlers are present in the `spiders` folder.
- The code to establish pipeline between scrapy data and mongodb is in the `settings.py` file.
- All the required python libraries required to do all the tasks are in the `requirements.txt` file.
- The mongo queries are in the `task2_queries.ipynb` file. The outputs of those cells can be seen there itself.
---
- Password for mongo database is present in the `.env` file.
---
### My approach to scrape this data and store it in a mongo collecion is pretty simple:
1. Get the CSS selector which selects all the products' elements on the product page.
2. Get the CSS selectors for respective fields (name, price, image url, product url etc.) and yield them as we iterate through all the products selected by the parent CSS selector.
3. Once everything from the page has been scraped, next I uploaded it to a mongodb collection using `pymongo` python library and the pipelines that are present in the `scrapy` library (code present in `pipelines.py` file).
4. Next we need to cater to pagination and for this, we need the CSS selector of "next page". This selector returns `None` if that particular element is not present in the HTML.
5. Got the page number from next page's url and used this to limit scraping process to 25 pages.
6. Same process was used to scrape both, the topwears' as well as footwears' page.
---
#### The logic behind all the queries in the second task are explained in the jupyter notebook in the form comments. Used mongodb's aggregate function to do most of the tasks as it's much faster and did the job as expected.