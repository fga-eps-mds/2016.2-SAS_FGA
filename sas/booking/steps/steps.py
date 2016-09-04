from aloe import step,world
from aloe_webdriver.util import find_field_by_id,find_any_field
from aloe_webdriver import TEXT_FIELDS

@step(r'I type in "(.*)" to "(.*)"')
def fill_bootstrap_field(step,text,field):
  words_list = field.lower().split()
  words_list.insert(0,"id")
  id_field = "_".join(words_list)
  date_field = find_any_field(world.browser,TEXT_FIELDS,id_field)
  date_field.send_keys(text)
