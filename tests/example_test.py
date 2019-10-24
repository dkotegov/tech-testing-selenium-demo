# -*- coding: utf-8 -*-

import os

import unittest
import urlparse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait


class Page(object):
    BASE_URL = 'http://tech-mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)    


class CreatePage(Page):
    PATH = '/blog/topic/create/'

    @property     
    def form(self):
        return CreateForm(self.driver)


class TopicPage(Page):
    @property
    def topic(self):
        return Topic(self.driver)


class BlogPage(Page):
    @property
    def topic(self):
        return Topic(self.driver)  


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '//input[@name="login"]'
    PASSWORD = '//input[@name="password"]'
    SUBMIT = '//span[text()="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход для участников"]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class TopMenu(Component):
    USERNAME = '//span[@class="username"]'

    def get_username(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USERNAME).text
        )  


class CreateForm(Component):
    BLOGSELECT = '//a[@class="chzn-single"]'
    OPTION = '//li[text()="{}"]'
    TITLE = '//input[@name="title"]'
    SHORT_TEXT = '//textarea[@name="text_short"]'
    MAIN_TEXT = '//textarea[@id="id_text"]'
    CREATE_BUTTON = '//button[contains(text(),"Создать")]'
    PUBLISH_CHECKBOX = '//input[@name="publish"]'

    def blog_select_open(self):
        blog = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.BLOGSELECT)
        )
        blog.click()

    def blog_select_set_option(self, option_text):
        self.driver.find_element_by_xpath(self.OPTION.format(option_text)).click()

    def set_title(self, title):
        self.driver.find_element_by_xpath(self.TITLE).send_keys(title)

    def set_short_text(self, short_text):
        self.driver.find_element_by_xpath(self.SHORT_TEXT).send_keys(short_text)
    
    def set_main_text(self, main_text):
        self.driver.find_element_by_xpath(self.MAIN_TEXT).send_keys(main_text)

    def submit(self):
        self.driver.find_element_by_xpath(self.CREATE_BUTTON).click()

    def set_unpublish(self):
        self.driver.find_element_by_xpath(self.PUBLISH_CHECKBOX).click()


class Topic(Component):
    TITLE = '//*[@class="topic-title"]/*'
    TEXT = '//*[@class="topic-content text"]'
    BLOG = '//*[@class="topic-blog"]'
    DELETE_BUTTON = '//a[@class="actions-delete"]'
    DELETE_BUTTON_CONFIRM = '//input[@value="Удалить"]'

    def get_title(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TITLE).text
        )

    def get_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TEXT).text
        )

    def open_blog(self):
        self.driver.find_element_by_xpath(self.BLOG).click()  

    def delete(self):
        self.driver.find_element_by_xpath(self.DELETE_BUTTON).click()
        confirm_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.DELETE_BUTTON_CONFIRM)
        )
        confirm_button.click()


class ExampleTest(unittest.TestCase):
    USERNAME = u'Дмитрий Котегов'
    USEREMAIL = 'kotegov_dima@mail.ru'
    PASSWORD = os.environ['PASSWORD']
    BLOG = 'Флудилка'
    TITLE = u'ЗаГоЛоВоК'
    MAIN_TEXT = u'Текст под катом! Отображается внутри топика!'

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

        user_name = auth_page.top_menu.get_username()
        self.assertEqual(self.USERNAME, user_name)

        create_page = CreatePage(self.driver)
        create_page.open()

        create_form = create_page.form
        create_form.blog_select_open()
        create_form.blog_select_set_option(self.BLOG)
        create_form.set_title(self.TITLE)
        create_form.set_main_text(self.MAIN_TEXT)
        create_form.set_unpublish()
        create_form.submit()

        topic_page = TopicPage(self.driver)
        topic_title = topic_page.topic.get_title()
        topic_text = topic_page.topic.get_text()
        self.assertEqual(self.TITLE, topic_title)
        self.assertEqual(self.MAIN_TEXT, topic_text)

        blog_page = BlogPage(self.driver)
        blog_page.topic.delete()
        topic_title = blog_page.topic.get_title()
        topic_text = blog_page.topic.get_text()
        self.assertNotEqual(self.TITLE, topic_title)
        self.assertNotEqual(self.MAIN_TEXT, topic_text)
