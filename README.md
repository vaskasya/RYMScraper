# RYMScraper
A Python-based tool to scrape information about artists and chart releases from RateYourMusic.

## Requirements

All Python module requirements can be found in the requirements.txt.
Other than that, you will need a version of [ChromeDriver](https://chromedriver.chromium.org/downloads). (The included version works with Google Chrome version 91.)
The ChromeDriver should sit either in the folder with the main.py script, or in your system PATH.

## Usage

Run python main.py with a URL and flag to specify whether the URL provided is a chart or artist URL.
The correct flag for URL type must be provided, otherwise the script will not run.

The --chart flag will prompt you to set the number of pages that should be searched. RYM charts top out at 250 pages.

For both commands, a GUI popup will ask what info should be saved to the file. 
The output file is a file called "chartOut.csv" located wherever the script is ran. It is encoded in UTF-8, and comma delimited.
It should be readable by default by Excel 2007 and later.

## Examples

python main.py https://rateyourmusic.com/artist/the-kinks --artist

Gets info about releases by the Kinks.

python main.py https://rateyourmusic.com/charts/top/album/all-time/g:punk/exc:live,archival/ --chart

Gets info about releases on the Best Punk Albums of All Time chart.

### Todo

1. More robust error checking. i.e - incorrect flags set, invalid parameters passed through GUI prompt.
2. Allow users to set their own output file.
