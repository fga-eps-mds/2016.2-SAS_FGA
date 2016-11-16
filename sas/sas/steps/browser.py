from contextlib import contextmanager

import aloe_webdriver
import aloe_webdriver.django
from aloe import around, world, step
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sas.settings import BASE_DIR
import os


@around.each_example
@contextmanager
def with_browser(scenario, outline, steps):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--lang=en")
    world.browser = webdriver.Chrome(os.path.join(BASE_DIR,
                                     "chromedriver", "chromedriver"),
                                     chrome_options=chrome_options)
    yield
    world.browser.quit()
    delattr(world, 'browser')
