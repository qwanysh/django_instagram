Feature: login

Scenario: wrong password login
  Given login page
  And superuser
  When I fill fields with wrong password
  And press submit button
  Then I see login page again
  And I see error in password field