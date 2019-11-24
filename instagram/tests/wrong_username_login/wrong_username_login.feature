Feature: login

Scenario: wrong username login
  Given login page
  When I fill fields with wrong username
  And press submit button
  Then I see login page again
  And I see error in username field