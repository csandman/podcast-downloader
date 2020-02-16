# Podbay Podcast Download

A web scraper made with scrapy to download all episodes of a given podcast and set all of the appropriate meta tags. Hopefully this might be useful for people to build an archive of their favorite podcasts

### Instructions

To use this package you must have python 3.7+ and have pipenv installed on your computer. To get this run `pip install pipenv`

Once you have pipenv, install this projects dependencies with `pipenv install`

Next run `scrapy crawl podcasts` and wait for them all to download! Once downloaded they will end up in the `output/{podcast name}` folder within the project directory.

Fair warning, podcast files are large so this will probably take a while, especially if there are a lot of episodes.

#### Tasks

[x] Download all podcasts from a series
[ ] Dynamic input URL
[ ] Episode numbering
[ ] Add cover images
[ ] Determine output file structure
