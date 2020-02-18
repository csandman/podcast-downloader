# Podbay Podcast Download

A web scraper made with scrapy to download all episodes of a given podcast and
set all of the appropriate meta tags. Hopefully this might be useful for people
to build an archive of their favorite podcasts

### Installation

To use this package you must have python 3.7+ and have pipenv installed on your
computer. To get this run `pip install pipenv`

Once you have pipenv, install this projects dependencies by navigating to your
project in the terminal and running `pipenv install`

### Running the download

Next run `pipenv run scrapy crawl podcasts` and wait for them all to download!
Once downloaded they will end up in the `output/{podcast name}` folder within
the project directory (custom output location is a work in progress).

Just to note, if this process fails at any point, you can run it again and it
will skip anything you've already downloaded, so that should make things a
little easier!

Fair warning, podcast files are large so this will probably take a while,
especially if there are a lot of episodes. Also this can congest your internet
connection so its better to run this when no one else is using it!

#### Tasks

-   [x] Download all podcasts from a series
-   [ ] Dynamic input URL list
-   [ ] Set all ID3 meta tags
    -   [x] Title
    -   [ ] Artist
        -   [ ] Album Artist
    -   [x] Description
        -   [ ] Lyrics? (itunes does it?)
    -   [ ] Track Number
    -   [ ] Release date
    -   [ ] Genre: Podcast
    -   [ ] Year
    -   [ ] Add sort title (remove and from normal title)
    -   [ ] Add cover images
        -   https://stackoverflow.com/questions/40515738/using-eyed3-to-embed-album-art-from-url
        -   https://stackoverflow.com/questions/38510694/how-to-add-album-art-to-mp3-file-using-python-3
-   [ ] Determine output file structure
    -   [ ] User defined output location
-   [ ] Scheduled task to download new episodes
-   [ ] Store images in the same directory (or a subdirectory of the podcast)
-   [ ] Replace illegal characters for all operating systems (keep the title the
        same)
    -   Windows: `\ / : * ? " < > |`
