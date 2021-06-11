import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
from bs4 import BeautifulSoup
import time
import argparse


#  Use this code at your own risk. RateYourMusic doesn't allow scraping, but they've still not released an API
#  despite promising to have one for years now. I figured this was fair game.


def createBox(name_dict, options, head_text):
    root = Tk()
    root.title("Make a selection")
    w = Label(root, text=head_text)
    w.pack()
    for option in options:
        j = IntVar()
        l = Checkbutton(root, text=option, variable=j)
        name_dict[option] = j
        l.pack(side=LEFT)
    root.mainloop()
    return name_dict


def stringWrite(*args):
    flattened_args = [item for sublist in args for item in sublist]
    s = ','.join(item.get_text() for item in flattened_args)
    s = '"' + s + '"'
    return s


def descriptorWrite(*args):
    # The descriptors on RYM are already comma separated, so I needed a separate function. Copying seemed easiest.
    flattened_args = [item for sublist in args for item in sublist]
    s = ''.join(item.get_text() for item in flattened_args)
    s = '"' + s + '"'
    return s


def getChart(input_url, page_number, name_dict):

    global release_type

    full_url = input_url + str(page_number) + '/#results'
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    releases = soup.find_all('div', class_="topcharts_itembox chart_item_release")
    release_types = ['Album', 'EP', 'Compilation', 'Single', 'Bootleg', 'Mixtape', 'DJ Mix']
    chart_title = soup.find('h1').get_text()

    # The release type is shown when searching for multiple release types, but not when searching for one.
    # Finding the release type and setting a variable.
    release_type_counter = 0
    for elem in release_types:
        if elem.lower() in chart_title.lower():
            release_type_counter = release_type_counter + 1
            release_type = elem


    for each_release in releases:
        # I didn't see a better way of doing this.
        title = each_release.find('a', class_="release").get_text()
        artist = each_release.find('a', class_="artist").get_text()
        release_date_broken = each_release.find('div', class_="topcharts_item_releasedate").get_text()
        # For some reason, RYM leaves a massive whitespace at the end of the release date. Has to be removed.
        if release_type_counter != 1:
            release_type = each_release.find('div', class_="chart_release_type").get_text()
        # Even more interestingly, this type element is attached to the date, making rstrip useless on its own.
        release_date = release_date_broken.replace(release_type, '')
        # First removing release type
        release_date = release_date.rstrip()
        # Then the trailing whitespace.
        rating = each_release.find('span', class_="topcharts_stat topcharts_avg_rating_stat").get_text()
        rating_count = each_release.find('span', class_="topcharts_stat topcharts_ratings_stat").get_text()
        review_count = each_release.find(class_="topcharts_stat topcharts_reviews_stat").get_text()
        primary_genre_soup = each_release.findAll(class_="genre topcharts_item_genres")
        primary_genres = stringWrite(primary_genre_soup)
        secondary_genre_soup = each_release.findAll(class_="genre topcharts_item_secondarygenres")
        secondary_genres = stringWrite(secondary_genre_soup)
        descriptors_soup = each_release.findAll(class_="topcharts_item_descriptors")
        descriptors = descriptorWrite(descriptors_soup)
        var_list = ["title", "artist", "release_date", "release_type", "rating", "rating_count", "review_count",
                    "primary_genres", "secondary_genres", "descriptors"]
        selection = []
        for x, y in zip(options, var_list):
            name_dict[y] = name_dict.pop(x)
        for key, value in name_dict.items():
            if value == 1:
                selection.append(eval(key))
        with open("chartOut.csv", "a", encoding="utf-8", newline='') as chartOut:
            w = csv.writer(chartOut)
            w.writerow(selection)
        for x, y in zip(options, var_list):
            name_dict[x] = name_dict.pop(y)



def rymArtistSearch(soup, selection):

    albumdiv = soup.find('div', id="disco_type_" + selection)

    for each_album in albumdiv.find_all(class_="disco_release"):
        title = each_album.find('a').get('title')
        try:
            release_date = each_album.find(attrs={'class': 'disco_year_ymd'}).get('title')
        except AttributeError:
            try:
                release_date = each_album.find(attrs={'class': 'disco_year_ym'}).get('title')
            except AttributeError:
                release_date = each_album.find(attrs={'class': 'disco_year_y'}).get('title')
            # Some releases are missing full info for the date.
        rating = each_album.find(attrs={'class': 'disco_avg_rating'}).text.strip()
        review_count = each_album.find(attrs={'class': 'disco_reviews'}).text.strip()
        rating_count = each_album.find(attrs={'class': 'disco_ratings'}).text.strip()
        release_info = [title, release_date, rating_count, review_count, rating]
        with open("chartOut.csv", "a", encoding="utf-8", newline='') as chartOut:
            w = csv.writer(chartOut)
            w.writerow(release_info)




headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 '
                  'Safari/537.36',
}

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ()[]āēīōūǖ'

letter_list = list(letters)

parser = argparse.ArgumentParser(description='Pulls information from RateYourMusic.com')

parser.add_argument('url', metavar='url', help='Provide a URL.')
parser.add_argument('--artist', action='store_true', help='Specifies that you have input an artist URL.')
parser.add_argument('--chart', action='store_true', help='Specifies that you have input a chart URL.')
ran_loop = 0
args = parser.parse_args()

if args.chart:
    input_url = args.url
    print('Enter number of pages to search \n')
    page = input()
    name_dict = {}
    options = ["Title", "Artist", "Release Date", "Release Type", "Avg. Rating", "Ratings", "Reviews", "Primary Genres",
               "Secondary Genres", "Descriptors"]
    head_text = "Select which headings should be added to the CSV"
    createBox(name_dict, options, head_text)
    name_dict = dict([(option, j.get()) for option, j in name_dict.items()])
    with open("chartOut.csv", "w", encoding="utf-8-sig", newline='') as chartOut:
        selection = []
        w = csv.writer(chartOut)
        for key, value in name_dict.items():
            if value == 1:
                selection.append(key)
        w.writerow(selection)
    for page_number in range(1, int(page) + 1):
        getChart(input_url, page_number, name_dict)


elif args.artist:
    input_url = args.url
    release_selection = []
    name_dict = {}
    options = ['Album', ' Live Album', 'EP', 'Single', 'Appears On', 'Compilation', 'V/A Compilation', 'Bootleg',
               'Mixtape', 'DJ Mix', 'Video']
    release_type_labels = ['s', 'l', 'e', 'i', 'a', 'c', 'v', 'b', 'm', 'j', 'd']
    release_selection_names = []
    release_dict = dict(zip(options,release_type_labels))
    head_text = "Select release types to pull info from"
    createBox(name_dict, options, head_text)
    name_dict = dict([(option, j.get()) for option, j in name_dict.items()])
    for key, value in name_dict.items():
        if value == 1:
            for key1, value1 in release_dict.items():
                if key1 == key:
                    release_selection.append(value1)
                    release_selection_names.append(key1)
    # I didn't want to use Selenium, but RYM doesn't show all the releases by default, and getting them to show by
    # sending a POST request is hard. Sending the existing JS code is much easier.

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Making Chrome run headless. At least this way we don't have to fake the User Agent, so that's something.
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(input_url)
    for x in release_type_labels:
        js_script = "RYMartistPage.expandDiscographySection('" + x + "');"
        js_script_check = "RYMartistPage.expandDiscographySection(\\'" + x + "\\');"
        # This is stupid, but the return string has escape characters, and this is the easiest way to search through it.
        # Hey, it works.
        if str(js_script_check) in str(driver.page_source.encode("utf-8")):
            driver.execute_script(js_script)

            # This expands all the categories.

    time.sleep(10)
    response = driver.page_source.encode("utf-8")
    driver.quit()
    soup = BeautifulSoup(response, 'html.parser')
    with open("chartOut.csv", "a", encoding="utf-8-sig", newline='') as chartOut:
        w = csv.writer(chartOut)
        w.writerow(['Title', 'Release Date', 'Ratings', 'Reviews', 'Avg. Rating'])
    type_increment = 0
    for selection in release_selection:
        with open("chartOut.csv", "a", encoding="utf-8", newline='') as chartOut:
            w = csv.writer(chartOut)
            selection_type = ['Release Type:' + str(release_selection_names[type_increment])]
            w.writerow(selection_type)
        rymArtistSearch(soup, selection)
        type_increment = type_increment + 1

else:
    print('Please specify the type of URL you are inputting by using one of the "--chart" or "--artist" flags.')