# -*- coding: utf-8 -*-

import services.startDriver
from services.startDriver import *
import time, sys, os
from pathlib import Path
from collections import OrderedDict
from io import StringIO
from html.parser import HTMLParser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def find_categories(driver):
    table = driver.find_elements_by_css_selector("#forum-body td a")
    categories_list = {}
    
    for i in range(len(table)):
        categories_list.update({table[i].get_attribute('innerHTML'): table[i].get_attribute('href')})
    return categories_list

def scrap_chapter(driver, url):
    driver.get(url)
    if url.startswith("file"):
        content = driver.find_element_by_css_selector('.container > .row:first-child')
    else:
        content = driver.page_source
    return content
    
def page_write(path, name, content):
    book_write = open(os.path.join(path, name + ".html"), "w")
    book_write.write(content)
    book_write.close()

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
            
            chapter_tab = driver.find_element_by_css_selector('#integration')
            
            chapters = OrderedDict()
            chapter_data= chapter_tab.find_elements_by_css_selector('a')
            for i, chapter in chapter_data:
                #chapters[strip_tags(chapter.get_attribute('innerHTML'))] = chapter.get_attribute('href')
                
                page_write(book_path, str(i+1) + "_" + strip_tags(chapter.get_attribute('innerHTML')), scrap_chapter(driver, chapter.get_attribute('href')))
                
            try:
                image_tab = driver.find_element_by_css_selector('#illustration')
                image_tab_content = '<meta charset="UTF-8">\n' + image_tab.get_attribute('innerHTML')
                
                page_write(book_path, "`1_image", image_tab_content)
            except:
                pass
            
            try:
                discussion_tab = driver.find_element_by_css_selector('#bbs')
                
                discussions = OrderedDict()
                discussion_data = discussion_tab.find_elements_by_css_selector('a')
                discussion_data = discussion_data.reverse()
                
                for i, discussion in discussion_data:
                    #discussions[strip_tags(discussion.get_attribute('innerHTML'))] = discussion.get_attribute('href')
                    
                    page_write(book_path, "d" +  str(i+1) + "_" + strip_tags(discussion.get_attribute('innerHTML')), scrap_chapter(driver, discussion.get_attribute('href')))
            except:
                pass
            
            
    
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
    print("\n")
    run()
