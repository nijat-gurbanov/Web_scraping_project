# Web_scraping_project
Web scraping project for university assignment

### Running scrapers:
For Selenium and Beautiful Soup, you do not have to do anything special. It is enough to run the file. In case of an error, you may try to change your driver location. I am using firefox driver in Selenium.

For scrapy, you have to run "links" spider first and save the result in links.csv file. Then you should run "players" spider and save the result in players.csv file. For running them, you can use following codes:
$ scrapy crawl links -O links.csv
$ scrapy crawl players -O players.csv
