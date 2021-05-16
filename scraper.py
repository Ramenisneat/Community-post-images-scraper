from selenium import webdriver
from time import sleep
import os
from decouple import config
from datetime import datetime
import subprocess
import argparse

def get_channel():
    op = webdriver.ChromeOptions()
    op.add_argument("headless")
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium/chromedriver",options=op) 
    driver.get(url= f"https://www.youtube.com/c/{config('CHANNEL')}/community")
    sleep(1)
    print(f"Got {config('CHANNEL')} channel")
    return driver

def scroll_to_bottom(driver):
    offset = 0 
    while True:
        current = offset
        driver.execute_script(f"window.scrollTo({offset},{offset+1000})")
        sleep(.5)
        offset = driver.execute_script("return window.pageYOffset")
        if offset == current:
            break
    sleep(1)
    print("scrolled to the bottom")
    

def get_posts(driver):
    container=driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-backstage-items/ytd-item-section-renderer/div[3]")
    posts = container.find_elements_by_class_name("style-scope ytd-backstage-post-renderer")

    post_links=[]

    for e in posts:
        e = e.find_element_by_id("content-attachment")
        e = e.find_element_by_tag_name('ytd-backstage-image-renderer')
        e = e.find_element_by_tag_name('a')

        post_links.append(e.get_attribute("href"))

    print("Got the links of posts")
    return post_links


def scraper(driver,post_links):

    if os.path.exists(f"{config('FOLDER')}"):
        os.system(f"rm -rf {config('FOLDER')}")

    os.mkdir(config('FOLDER'))
    os.chdir(config('FOLDER'))
    
    counter = 1
    with open("urls.txt",mode="w") as file:
        for url in post_links[::-1]:
            if url == None:
                print("none")
                post_links.remove(url)
                continue
            print(url)
            driver.get(url=url)
            i = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-backstage-items/ytd-item-section-renderer/div[3]/ytd-backstage-post-thread-renderer/div[1]/ytd-backstage-post-renderer/div[1]/div[2]/div[2]/ytd-backstage-image-renderer/div/yt-img-shadow/img")
            link = i.get_attribute("src")
            os.system(f"curl {link} > image{counter}.png")
            counter+=1
            file.write(url+"\n")


def updater(driver, post_links):

    print(datetime.now())
    sleep(2)

    os.chdir(config('FOLDER'))
  
    num = int(subprocess.check_output("ls | wc -l", shell=True)) - 1
    lines = []
    with open('urls.txt') as f:
        lines = f.read().splitlines()
    print(num)
    with open("urls.txt",mode="a") as file:
        for url in post_links[:11]:
            if url == None: continue
            if url in lines:
                print(f"already got {url}")
            else:
                driver.get(url=url)
                src = (driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-backstage-items/ytd-item-section-renderer/div[3]/ytd-backstage-post-thread-renderer/div[1]/ytd-backstage-post-renderer/div[1]/div[2]/div[2]/ytd-backstage-image-renderer/div/yt-img-shadow/img")).get_attribute("src")
                print("making "+url)
                os.system(f"curl {src} > image{num+1}.png")
                file.write(url+"\n")


def main():
    parser = argparse.ArgumentParser(description= "Youtube community post images scraper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', help='Scrape all of the available posts', action='store_true')
    group.add_argument('-u', help="Update upon existing scraped images. (Use only after executing '-s')", action='store_true')
    args = parser.parse_args()

    driver = get_channel()

    if args.s:
        scroll_to_bottom(driver)
        post_links = get_posts(driver)
        scraper(driver,post_links)

    elif args.u:
        driver.execute_script(f"window.scrollTo(0,500)")
        sleep(2)
        post_links = get_posts(driver)
        updater(driver,post_links)
    
    print("done")
        

if __name__ == "__main__":
    main()    
