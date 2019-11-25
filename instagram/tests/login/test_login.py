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
def check_post_list_page(live_server, browser):
    assert browser.url == live_server.url + reverse('publications:post_list')


@then('I see username on sidebar')
def check_post_list_page(live_server, browser):
    username_wrapper = \
        browser.find_by_css('body > main > div > aside > div.sidebar-account-wrapper > div > div > a > span')
    assert username_wrapper.text == 'admin'


@scenario('login.feature', 'wrong username login')
def test_wrong_username_login(live_server):
    return live_server


@when('I fill fields with wrong username')
def fill_fields(browser, admin_user):
    browser.fill('username', 'wrong_username')
    browser.fill('password', 'password')


@then('I see login page again')
def check_login_page(live_server, browser):
    assert browser.url == live_server.url + reverse('users:login')


@then('I see error in username field')
def check_username_error(browser):
    assert 'Неверное имя пользователя' in browser.find_by_css('body > main > div > div > form > div.form-group.error > p').text


@scenario('login.feature', 'wrong password login')
def test_wrong_password_login(live_server):
    return live_server


@when('I fill fields with wrong password')
def fill_fields(browser, admin_user):
    browser.fill('username', 'admin')
    browser.fill('password', 'wrong_password')


@then('I see error in password field')
def check_password_error(browser):
    assert 'Неверный пароль' in browser.find_by_css('body > main > div > div > form > div.form-group.error > p').text
