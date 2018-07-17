from selenium import webdriver
from time import sleep
from PIL import Image
from datetime import datetime
import os
from shutil import move
import sys
from zipfile import ZipFile
from os import listdir, unlink, makedirs
from os.path import basename


def start_scrape(url, pages):
    start_time = 'Joomag__' + str(datetime.now().strftime('%d-%m-%Y__%H:%M:%S'))
    down_dir = '/Novus_flask/downloaded/' + start_time
    makedirs(down_dir)

    yield 'start time: ' + start_time + '<br/>\n'
    yield 'starting browser<br/>\n'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                               chrome_options=chrome_options)

    yield 'scraping url: ' + url + '<br/>\n'
    yield 'attempting to scrape {} pages<br/>\n'.format(pages)
    browser.get(url)
    browser.set_window_size(2000, 2000)

    yield 'logging in<br/>\n'
    username = browser.find_element_by_name('ctl00$ContentPlaceHolder1$txtEmailAddress')
    username.send_keys('elriza@novusgroup.co.za')
    password = browser.find_element_by_name('ctl00$ContentPlaceHolder1$txtPassword')
    password.send_keys('q6mzajv6')

    submit = browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnSubmit"]')
    submit.click()
    yield 'login successful<br/>\n'

    # iterate over the total number of pages and capture
    pages = int(pages) + 1

    for page in range(0, int(pages)):
        if page % 2 == 0:
            yield 'browsing to ' + url + '/' + str(page) + '<br/>\n'
            browser.get(url + '/' + str(page))
            browser.set_window_size(4000, 2000)
            sleep(5)

            yield 'rendering page<br/>\n'
            try:
                elem = browser.find_element_by_xpath('//*[@id="landscape"]')
                elem.click()
                elem.click()
                sleep(5)
            except Exception as e:
                yield str(e)
                sys.exit('fatal error')

            # label each page with page number
            browser.save_screenshot('/Novus_flask/downloaded/{}/page{}.png'.format(start_time, page))

            # downsize & convert image
            im = Image.open('/Novus_flask/downloaded/{}/page{}.png'.format(start_time, page))
            im.thumbnail((4000, 4000))
            im = im.convert('RGB')
            im.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page))
            unlink('/Novus_flask/downloaded/{}/page{}.png'.format(start_time, page))

            original = Image.open('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page))

            # Crop off black edges
            left = 0
            top = 0
            right = 3200
            bottom = 1960
            cropped_example = original.crop((left, top, right, bottom))

            # Get the left page
            left__a = 0
            top__a = 0
            right__a = 1600
            bottom__a = 1960
            cropped_example__a = original.crop((left__a, top__a, right__a, bottom__a))
            cropped_example__a.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page))

            # Get the right page
            left__b = 1600
            top__b = 0
            right__b = 3200
            bottom__b = 1960
            cropped_example__b = original.crop((left__b, top__b, right__b, bottom__b))
            cropped_example__b.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page + 1))
            yield 'saving to file: page{}.jpeg & page{}.jpeg'.format(page, page + 1) + '<br/>\n'

    # close browser only after iteration of all pages is complete
    browser.quit()

    # rename first page
    if 'page0.jpeg' in os.listdir('/Novus_flask/downloaded/{}'.format(start_time)):
        unlink('/Novus_flask/downloaded/{}/page1.jpeg'.format(start_time))
        move('/Novus_flask/downloaded/{}/page0.jpeg'.format(start_time),
             '/Novus_flask/downloaded/{}/page1.jpeg'.format(start_time))

    # delete last page if page number is odd (black image)
    if pages % 2 != 0:
        yield 'removing last blank page{}.jpeg'.format(pages) + '<br/>\n'
        unlink('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pages))

    # post start/end time for analysis
    end_time = str(datetime.now().strftime('%d-%m-%Y__%H:%M:%S'))
    yield 'end time:' + end_time + '<br/>\n'
    
    # TODO: zip the directory 
    '''
    working_dir = '/Novus_flask/downloaded/'
    with ZipFile(start_time + '.zip', mode='a') as zf:
        for f in listdir(working_dir):
            zf.write(working_dir + f, basename(f))
    yield 'file zipped'
    '''

    yield '<br/>\n'
    yield 'complete'
    yield '<br/>\n'
    yield '<a href=ftp://flask.novusgroup.co.za:2121>ftp://flask.novusgroup.co.za:2121</a>'

