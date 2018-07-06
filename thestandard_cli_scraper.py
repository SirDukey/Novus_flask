from selenium import webdriver
from time import sleep
from PIL import Image
from datetime import datetime
import os
import shutil


def start():

    start_time = str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    print('#========| NOVUS GROUP (PTY)LTD |========#')
    print('#                                        #')
    print('# Scraping tool for the java application #')
    print('# used on "epaper.standardmedia.co.ke"   #')
    print('# - paste in the publication url         #')
    print('# - specify the total pages              #')
    print('#                                        #')
    print('#========================================#')
    print()

    # sysargs to populate the url & pages variables
    url = input('What is the url to scrape: ')
    #url = 'https://epaper.standardmedia.co.ke/StandardGroupLimited/TheStandard/TheStandard/issue/100/2062018100502874'
    #pages = 2
    pages = int(input('How many pages to scrape: '))
    print()
    print('start time:', start_time)
    print('starting browser')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox') # required when running as root user
    browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                               chrome_options=chrome_options)

    print('scraping url:', url)
    print('attempting to scrape {} pages'.format(pages))
    browser.get(url)
    browser.set_window_size(2000, 2000)

    print('logging in')
    username = browser.find_element_by_name('ctl00$ContentPlaceHolder1$txtEmailAddress')
    username.send_keys('elriza@novusgroup.co.za')
    password = browser.find_element_by_name('ctl00$ContentPlaceHolder1$txtPassword')
    password.send_keys('q6mzajv6')

    submit = browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnSubmit"]')
    submit.click()
    print('login successful')

    # iterate over the total number of pages and capture
    pages = pages + 1

    for page in range(0, int(pages)):
        if page % 2 == 0:
            print('browsing to', url + '/' + str(page))
            browser.get(url + '/' + str(page))
            browser.set_window_size(4000, 2000)

            print('rendering page')
            try:
                #browser.find_element_by_css_selector('#landscape').click()
                #browser.find_element_by_css_selector('#landscape').click()
                elem = browser.find_element_by_css_selector('#landscape')
                elem.click()
                elem.click()
                sleep(5)
            except Exception as e:
                print(e)          
                break 

            # label each page with page number
            browser.save_screenshot('page{}.png'.format(page))

            # downsize & convert image
            im = Image.open('page{}.png'.format(page))
            im.thumbnail((4000, 4000))
            im = im.convert('RGB')
            im.save('page{}.jpeg'.format(page))
            os.unlink('page{}.png'.format(page))

            original = Image.open('page{}.jpeg'.format(page))

            # Crop off black edges
            width, height = im.size
            left = 0
            top = 0
            right = 3200
            bottom = 1960
            cropped_example = original.crop((left, top, right, bottom))

            # Get the left page
            width_A, height_A = cropped_example.size
            left__a = 0
            top__a = 0
            right__a = 1600
            bottom__a = 1960
            cropped_example__a = original.crop((left__a, top__a, right__a, bottom__a))
            cropped_example__a.save('page{}.jpeg'.format(page))

            # Get the right page
            width_B, height_B = cropped_example.size
            left__b = 1600
            top__b = 0
            right__b = 3200
            bottom__b = 1960
            cropped_example__b = original.crop((left__b, top__b, right__b, bottom__b))
            cropped_example__b.save('page{}.jpeg'.format(page + 1))
            print('saving to file: page{}.jpeg & page{}.jpeg'.format(page, page + 1))

    # close browser only after iteration of all pages is complete
    browser.quit()

    # rename first page
    if 'page0.jpeg' in os.listdir():
        os.unlink('page1.jpeg')
        shutil.move('page0.jpeg', 'page1.jpeg')

    # delete last page if page number is odd (black image)
    if pages % 2 != 0:
        print('removing last blank page{}.jpeg'.format(pages))
        os.unlink('page{}.jpeg'.format(pages))

    print()
    print('complete')
    print()

    # post start/end time for analysis
    end_time = str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    print('start time:', start_time)
    print('end time:', end_time)
    print()
    prompt = input('press "q" to quit or "r" to run another: ')
    if prompt == 'r':
        start()


if __name__ == '__main__':
    start()
