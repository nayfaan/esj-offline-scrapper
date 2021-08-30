# -*- coding: utf-8 -*-

import services.startDriver
from services.startDriver import *
import time, sys, os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_categories(driver):
    table = driver.find_elements_by_css_selector("#forum-body td a")
    categories_list = {}
    
    for i in range(len(table)):
        categories_list.update({table[i].get_attribute('innerHTML'): table[i].get_attribute('href')})
    return categories_list

def scrap(driver):
    books = find_categories(driver)
    
    for category in books:
        Path(os.path.join(os.path.sep, ROOT_DIR,'output', category)).mkdir(parents=True, exist_ok=True)
        driver.get(books[category])
        books.update({category: find_categories(driver)})
        
        for book in books[category]:
            book_path = os.path.join(os.path.sep, ROOT_DIR,'output', category,book)
            Path(book_path).mkdir(parents=True, exist_ok=True)
            
            driver.get(books[category][book])
            
            image_tab = driver.find_element_by_css_selector('#illustration')
            image_tab_content = '<meta charset="UTF-8">\n' + image_tab.get_attribute('innerHTML')
            
            book_write = open(os.path.join(book_path, str(book) + ".html"), "w")
            book_write.write(image_tab_content)
            book_write.close()
    
def run():
    driver = services.startDriver.start()
    
    
    esj_home = 'file://' + os.path.join(os.path.sep, ROOT_DIR,'esj/bbs.html')
    
    driver.get(esj_home)
    
    try:
        scrap(driver)
        
    except:
        pass
    finally:
        driver.close()

if __name__ == "__main__":
    run()
