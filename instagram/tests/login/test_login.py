from pytest_bdd import scenario, given, when, then
from django.urls import reverse


@scenario('login.feature', 'authorization as admin')
def test_login(live_server):
    return live_server


@given('superuser')
def get_superuser(admin_user):
    return admin_user


@given('login page')
def get_login_page(live_server, browser):
    browser.visit(live_server.url + reverse('users:login'))


@when('I fill fields')
def fill_fields(browser, admin_user):
    browser.fill('username', 'admin')
    browser.fill('password', 'password')


@when('press submit button')
def press_submit_button(browser):
    browser.find_by_css('body > main > div > div > form > div:nth-child(4) > button').click()


@then('I see post list page')
def check_home_page(live_server, browser):
    assert browser.url == live_server.url + reverse('publications:post_list')
