# -*- coding: utf-8 -*-

from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    # driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.get("https://park.vk.company/")
    driver.quit()
