Feature: registration

Scenario: register new user
  Given registration page
  When I fill fields
  And press submit button
  Then I see post list page
  And I see username on sidebar