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

start_time = 'Joomag__' + str(datetime.now().strftime('%d-%m-%Y__%H:%M:%S'))


def start_scrape(url, pages):
    try:

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

        # close subscription pop-up
        try:
            sleep(1)
            popup_x = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[1]/span')
            sleep(1)
            popup_x.click()
        except Exception as e:
            yield str(e) + '<br/>\n'
            yield 'click on the back button and retry...<br/>\n'

        # click on fullscreen button
        fullscreen_btn = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div[2]')
        fullscreen_btn.click()
        sleep(1)

        # iterate over the total number of pages and capture
        for page in range(0, int(pages)):
            if page % 2 == 0:

                browser.set_window_size(4000, 2000)
                sleep(5)
                yield 'rendering page<br/>\n'

                # label each page with page number
                browser.save_screenshot('/Novus_flask/downloaded/{}/page{}.png'.format(start_time, page))

                # downsize & convert image
                im = Image.open('/Novus_flask/downloaded/{}/page{}.png'.format(start_time, page))
                im.thumbnail((4000, 4000))
                im = im.convert('RGB')
                im.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page))
                unlink('/Novus_flask/downloaded/{}/page{}.png'.format(start_time, page))

                original = Image.open('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page))

                # Get the left page
                left__a = 550
                top__a = 15
                right__a = 1930
                bottom__a = 1960
                cropped_example__a = original.crop((left__a, top__a, right__a, bottom__a))
                cropped_example__a.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page))
                yield 'saving to file<br/>\n'

                # Get the right page
                left__b = 1930
                top__b = 15
                right__b = 3306
                bottom__b = 1960
                cropped_example__b = original.crop((left__b, top__b, right__b, bottom__b))
                cropped_example__b.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, page + 1))
                yield 'saving to file: page{}.jpeg & page{}.jpeg'.format(page, page + 1) + '<br/>\n'

                # Next page
                try:
                    next_btn = browser.find_element_by_css_selector('div.j-slider-button:nth-child(2)')
                    next_btn.click()
                    yield 'next page<br/>\n'
                except:
                    yield 'end of pages<br/>\n'
                    break

        # close browser only after iteration of all pages is complete
        browser.quit()

    except Exception as e:
        yield str(e) + '<br/>\n'
        yield 'click on the back button and retry...<br/>\n'

    # join the first two pages and crop
    class pageClass(object):
        def __init__(self, pageNum):
            self.pageNum = pageNum

        def join_and_crop(self, pageNum):
            first_im = Image.open('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pageNum[0]))
            second_im = Image.open('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pageNum[1]))
            size = first_im.size
            width = size[0] * 2
            height = size[1]
            size = width, height
            single_im = Image.new('RGB', size, 'white')
            single_im.paste(first_im)
            single_im.paste(second_im, (1380, 0))
            box = (694, 0, 2064, 1960)
            cropped = single_im.crop(box)
            cropped.save('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pageNum[1]))
            unlink('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pageNum[0]))
            yield 'pages joined and cropped<br/>\n'

    pages = pages + 1
    first_pages = pageClass((0, 1))
    last_pages = pageClass((pages - 1, pages))

    try:
        first_pages.join_and_crop(pageNum=(0, 1))
        last_pages.join_and_crop(pageNum=(pages - 1, pages))
        move('/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pages), '/Novus_flask/downloaded/{}/page{}.jpeg'.format(start_time, pages - 1))
    except Exception as e:
        yield str(e) + '<br/>\n'
        yield 'click on the back button and retry...<br/>\n'

    # post start/end time for analysis
    end_time = str(datetime.now().strftime('%d-%m-%Y__%H:%M:%S'))
    yield 'end time:' + end_time + '<br/>\n'

    # zip the files and remove the jpeg images
    try:
        working_dir = '/Novus_flask/downloaded/' + start_time + '/'
        zip_dir = '/Novus_flask/zip/'
        with ZipFile(zip_dir + start_time + '.zip', mode='a') as zf:
            for f in listdir(working_dir):
                zf.write(working_dir + f, basename(f))
        move(zip_dir + start_time + '.zip', working_dir + start_time + '.zip')
        yield 'file zipped'
        for f in listdir(working_dir):
            if 'jpeg' in f:
                unlink(working_dir + f)
    except Exception as e:
        yield str(e)

    yield '<br/>\n'
    yield 'complete'
    yield '<br/>\n'
    yield '<a href=ftp://flask.novusgroup.co.za:2121/{}/{}>' \
          'download file</a>'.format(start_time, start_time + '.zip')
