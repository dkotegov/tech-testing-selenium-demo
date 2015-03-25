# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if __name__ == '__main__': 
  driver = webdriver.Remote(
    command_executor='http://127.0.0.1:5555/wd/hub',
    desired_capabilities=DesiredCapabilities.FIREFOX )
  driver.get("http://ftest.stud.tech-mail.ru/")
  driver.quit()