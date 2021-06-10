# RYMScraper
A Python-based tool to scrape information about artists and chart releases from RateYourMusic.

## Requirements

All Python module requirements can be found in the requirements.txt.
Other than that, you will need a version of [ChromeDriver](https://chromedriver.chromium.org/downloads). (The included version works with Google Chrome version 91.)
The ChromeDriver should sit either in the folder with the main.py script, or in your system PATH.

## Usage

Run python main.py with a URL and flag to specify whether the URL provided is a chart or artist URL.

Examples:

python main.py https://rateyourmusic.com/artist/the-kinks --artist
Gets info about releases by the Kinks.

python main.py https://rateyourmusic.com/charts/top/album/all-time/g:punk/exc:live,archival/ --chart
Gets info about releases on the Best Punk Albums of All Time chart.

