from aloe import step, world
from aloe_webdriver.util import find_field_by_id, find_any_field, find_field_by_value
from aloe_webdriver import TEXT_FIELDS
from selenium.common.exceptions import NoSuchElementException
from user.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.test import Client


@step(r'I type in "(.*)" to "(.*)"')
def fill_bootstrap_field(step, text, field):
	words_list = field.lower().split()
	words_list.insert(0, "id")
	id_field = "_".join(words_list)
	date_field = find_any_field(world.browser, TEXT_FIELDS, id_field)
	date_field.send_keys(text)


@step(r'I type in "(.*)" to id "(.*)"')
def fill_bootstrap_field(step, text, id_field):
	date_field = find_any_field(world.browser, TEXT_FIELDS, id_field)
	date_field.send_keys(text)


@step(r'I click on an element with id of "(.*)"')
def click_on_element_by_id(step, id):
	try:
		elem = world.browser.find_element_by_id(id)
	except NoSuchElementException:
		raise AssertionError("Element with ID '{}' not found.".format(id))
	elem.click()


@step(r'I click on an element "(.*)" called "(.*)"')
def click_on_element_by_value(step, value, typeelement):
	try:
		text = find_field_by_value(world.browser, typeelement, elementtext)
	except NoSuchElementException:
		raise AssertionError("Element not found.")
	text.click()


@step(r'I register the user "(.*)" with the password "(.*)" and registration number "(.*)"')
def register_user(step, username, password,registration_number):
	user = UserProfile()
	user.user = User()				
	user.registration_number = registration_number	
	user.user.email = username
	user.user.username = username
	user.user.first_name = "Usuário"
	user.user.set_password(password)
	user.save()


@step(r'I login in with email "(.*)" and password "(.*)"')
def login_user(step, email, password):
	step.given("I visit site page \"/\"")
	c = Client()
	response = c.login(username=email, password=password)
	cookies = {}
	for co in c.cookies.values():
		cookies['name'] = co.key
		cookies['value'] = co.value
		world.browser.add_cookie(cookies)
	world.browser.refresh()
