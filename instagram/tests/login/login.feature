Feature: login

Scenario: authorization as admin
  Given superuser
  And login page
  When I fill fields
  And press submit button
  Then I see post list page
  And I see username on sidebar

Scenario: wrong username login
  Given login page
  When I fill fields with wrong username
  And press submit button
  Then I see login page again
  And I see error in username field

Scenario: wrong password login
  Given login page
  And superuser
  When I fill fields with wrong password
  And press submit button
  Then I see login page again
  And I see error in password field