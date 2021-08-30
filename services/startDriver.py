from selenium import webdriver
from selenium import *
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def start():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    return webdriver.Chrome(desired_capabilities=caps, executable_path='./services/chromedriver')

if __name__ == "__main__":
    pass
