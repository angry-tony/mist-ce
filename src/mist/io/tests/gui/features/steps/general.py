from behave import *
from time import time, sleep


@when(u'I visit mist.io')
def visit(context):
    end_time = time() + 60
    while time() < end_time:
        context.browser.get(context.mist_url)
        sleep(1)
        state = context.browser.execute_script("return document.readyState")
        if state == "complete":
            return
        sleep(1)
    assert False, u'Splash page took longer than 40 seconds to load'

@when(u'I wait for {seconds} seconds')
def wait(context, seconds):
    sleep(int(seconds))


@when(u'I click the "{text}" button')
def click_button(context, text):
    buttons = context.browser.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if button.text == text:
            button.click()
            return

    assert False, u'Could not find %s button' % text


@when(u'I click the button that contains "{text}"')
def click_button(context, text):
    buttons = context.browser.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if text in button.text:
            button.click()
            return

    assert False, u'Could not find button that contains %s' % text



@when(u'I click the "{text}" button inside the "{popup}" popup')
def click_button_within_popup(context, text, popup):
    popups = context.browser.find_elements_by_class_name("ui-popup-active")
    for pop in popups:
        if popup in pop.text:
            buttons = pop.find_elements_by_class_name("ui-btn")
            for button in buttons:
                if text in button.text:
                    button.click()
                    return

    assert False, u'Could not find %s button in %s popup' % (text, popup)


@when(u'I click the "{text}" button inside the "{panel_title}" panel')
def click_button_within_panel(context, text, panel_title):
    panels = context.browser.find_elements_by_class_name("ui-panel-open")
    if not panels:
        assert False, u'No open panels found. Maybe the driver got refocused or the panel failed to open'

    found_panel = None
    for panel in panels:
        header = panel.find_element_by_tag_name("h1")
        if panel_title in header.text:
            found_panel = panel
            import ipdb
            break

    if not found_panel:
        assert False, u'Panel with Title %s could not be found. Maybe the driver got refocused or the panel ' \
                      u'failed to open or there is no panel with that title' % panel_title

    buttons = found_panel.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if text in button.text:
            button.click()
            return

    assert False, u'Could not find %s button inside %s panel' % (text, panel_title)


@then(u'the title should be "{text}"')
def assert_title_is(context, text):
    assert text == context.browser.title


@then(u'the title should contain "{text}"')
def assert_title_contains(context, text):
    assert text in context.browser.title