from aloe import step,world
from aloe_webdriver.util import find_field_by_id,find_any_field
from aloe_webdriver import TEXT_FIELDS
from booking.models import UserProfile

@step(r'I type in "(.*)" to "(.*)"')
def fill_bootstrap_field(step,text,field):
  words_list = field.lower().split()
  words_list.insert(0,"id")
  id_field = "_".join(words_list)
  date_field = find_any_field(world.browser,TEXT_FIELDS,id_field)
  date_field.send_keys(text)

@step(r'I register the user "(.*)" with the password "(.*)"')
def fill_bootstrap_field(step,username,password):
  user = UserProfile()
  user.registration_number = "23412"
  user.user.email = "sdsade@dasd.com"
  user.user.first_name = "Pudim"
  user.user.username = username
  user.user.set_password(password)
  user.save()
