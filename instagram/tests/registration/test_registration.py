from pytest_bdd import scenario, given, when, then
from django.urls import reverse


@scenario('registration.feature', 'register new user')
def test_registration(live_server):
    return live_server


@given('registration page')
def get_registration_page(live_server, browser):
    browser.visit(live_server.url + reverse('users:register'))


@when('I fill fields')
def fill_fields(browser):
    browser.fill('username', 'test')
    browser.fill('password', 'test')
    browser.fill('password_confirm', 'test')


@when('press submit button')
def press_submit_button(browser):
    browser.find_by_css('body > main > div > div > form > div:nth-child(8) > button').click()


@then('I see post list page')
def check_post_list_page(live_server, browser):
    assert browser.url == live_server.url + reverse('publications:post_list')


@then('I see username on sidebar')
def check_username_on_sidebar(browser):
    username_wrapper = browser.find_by_css('body > main > div > aside > div.sidebar-account-wrapper > div > div > a > span')
    assert username_wrapper.text == 'test'
