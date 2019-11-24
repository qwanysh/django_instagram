from pytest_bdd import scenario, given, when, then
from django.urls import reverse


@scenario('wrong_password_login.feature', 'wrong password login')
def test_failed_login(live_server):
    return live_server


@given('login page')
def get_login_page(live_server, browser):
    browser.visit(live_server.url + reverse('users:login'))


@given('superuser')
def get_superuser(admin_user):
    return admin_user


@when('I fill fields with wrong password')
def fill_fields(browser, admin_user):
    browser.fill('username', 'admin')
    browser.fill('password', 'wrong_password')


@when('press submit button')
def press_submit_button(browser):
    browser.find_by_css('body > main > div > div > form > div:nth-child(4) > button').click()


@then('I see login page again')
def check_login_page(live_server, browser):
    assert browser.url == live_server.url + reverse('users:login')


@then('I see error in password field')
def check_password_error(browser):
    assert 'Неверный пароль' in browser.find_by_css('body > main > div > div > form > div.form-group.error > p').text
