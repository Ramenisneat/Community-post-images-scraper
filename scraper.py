#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
from dotenv import load_dotenv
from datetime import datetime
import subprocess
import argparse



def get_channel(CHANNEL):
    op = webdriver.ChromeOptions()
    op.add_argument("headless")
    driver = webdriver.Chrome(options=op) 
    driver.get(url= f"https://www.youtube.com/@{CHANNEL}/community")
    sleep(1)
    print(f"Got {CHANNEL} channel")
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
    posts = driver.find_elements(By.XPATH, "//div[@id='contents']//div[@id='content-attachment']//a[1]")
    post_links=[]
    for e in posts:
        link = e.get_attribute("href")
        if "post/" in link:
            post_links.append(link)

    print("Got the links of posts")
    # print(post_links)
    return post_links


def scraper(driver,post_links,FOLDER):

    if os.path.exists(f"{FOLDER}"):
        os.system(f"rm -rf {FOLDER}")

    os.mkdir(FOLDER)
    os.chdir(FOLDER)
    
    counter = 1
    with open("urls.txt",mode="w") as file:
        for url in post_links[::-1]:
            print("making " + url)
            driver.get(url=url)
            sleep(1)
            i = driver.find_element(By.XPATH, "//div[@id='image-container']//img")
            link = i.get_attribute("src")
            os.system(f"curl {link} > image{counter}.png")
            sleep(1)
            counter+=1
            file.write(url+"\n")


def updater(driver, post_links, FOLDER):

    print(datetime.now())
    sleep(2)

    os.chdir(FOLDER)
  
    num = int(subprocess.check_output("cat urls.txt | wc -l", shell=True)) 
    lines = []
    with open("urls.txt",mode="r") as file:
        lines = file.read().splitlines()
        print(num)
    
    with open("urls.txt",mode="a") as file:
        for url in post_links[::-1]:
            if url in lines:
                print(f"already got {url}")
            else:
                driver.get(url=url)
                sleep(1)
                src = (driver.find_element(By.XPATH, "//div[@id='image-container']//img")).get_attribute("src")
                print("making "+url)
                num = num + 1
                os.system(f"curl {src} > image{num}.png")
                sleep(1)
                print("finished this one")
                file.write(url+"\n")


def main():
    load_dotenv()
    CHANNEL = os.getenv("CHANNEL")
    FOLDER = os.getenv("FOLDER")

    parser = argparse.ArgumentParser(description= "Youtube community post images scraper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', help='Scrape all of the available posts', action='store_true')
    group.add_argument('-u', help="Update upon existing scraped images. (Use only after executing '-s')", action='store_true')
    args = parser.parse_args()

    driver = get_channel(CHANNEL)

    if args.s:
        scroll_to_bottom(driver)
        post_links = get_posts(driver)
        scraper(driver,post_links,FOLDER)

    elif args.u:
        driver.execute_script(f"window.scrollTo(0,2000)")
        sleep(1)
        post_links = get_posts(driver)
        updater(driver,post_links,FOLDER)
    
    print("done")
        

if __name__ == "__main__":
    main()    
