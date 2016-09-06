from contextlib import contextmanager

import aloe_webdriver
import aloe_webdriver.django
from aloe import around, world,step
from selenium import webdriver
from sas.settings import BASE_DIR
import os

@around.each_example
@contextmanager
def with_browser(scenario,outline,steps):
  world.browser = webdriver.Chrome(os.path.join(BASE_DIR,"chromedriver","chromedriver"))
  yield
  world.browser.quit()
  delattr(world, 'browser')
