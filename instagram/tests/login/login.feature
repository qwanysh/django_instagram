Feature: login

Scenario: authorization as admin
  Given superuser
  And login page
  When I fill fields
  And press submit button
  Then I see post list page