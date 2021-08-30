import services.startDriver
from services.startDriver import *
import csv
import time

def initiate_driver(driver, url):
    driver.get(url)
    
def login(driver,username,password):
    WebDriverWait(driver, timeout=10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#user_login")))
    
    username_field = driver.find_element_by_css_selector("#user_login")
    username_field.clear()
    username_field.send_keys(username)
    
    WebDriverWait(driver, timeout=10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#user_pass")))
    
    password_field = driver.find_element_by_css_selector("#user_pass")
    password_field.clear()
    password_field.send_keys(password)
    time.sleep(0.3)
    password_field.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, timeout=60).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#wpcontent")))
    
def output_csv(ids):
    with open('output/output_url.csv', 'w', newline='') as csvfile:
        output = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in ids:
            output.writerow(row)
            print(row)

def scrap(driver,ids):
    
    ids_temp = ids
    
    try:
        for row in ids_temp:
            driver.get(row[0])
            WebDriverWait(driver, timeout=120).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#sample-permalink > a")))
            url_prod = driver.find_element_by_css_selector("#sample-permalink > a").get_attribute("href")
            row.append(url_prod)
    except:
        print("Timeout Error")
    finally:
        output_csv(ids_temp)
    
def run():
    ids=[]
    
    with open('./input/ids.csv', newline='') as csvfile:
        ids_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        for row in ids_csv:
            url_edit = "https://facedrivesupply.com/wp-admin/post.php?post=" + row[0] + "&action=edit"
            ids.append(url_edit.split())
    
    driver = services.startDriver.start()
    initiate_driver(driver, "https://facedrivesupply.com/wp-admin/edit.php?post_type=product")
    
    with open('./input/credentials.txt','r') as f:
        credentials = f.read().splitlines()
    
    
    login(driver,credentials[0],credentials[1])
    
    try:
        scrap(driver,ids)
    except:
        pass
    finally:
        driver.close()

if __name__ == "__main__":
    run()
