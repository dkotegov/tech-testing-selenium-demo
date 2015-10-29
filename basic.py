# -*- coding: utf-8 -*-

from selenium import webdriver

if __name__ == '__main__':
    # driver = webdriver.Chrome('./chromedriver')
    driver = webdriver.Firefox()
    driver.get("http://ftest.stud.tech-mail.ru/")
    driver.quit()
