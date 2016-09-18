Feature: Delete

Background:
  Given I register the user "lucas@gmail.com" with the password "123456"

Scenario: User already registered and wants to delete their account
  When I visit site page "/"
  Then I should see an element with id of "enter-button"
  Then I click on an element with id of "enter-button"
  And I fill in "Email" with "lucas@gmail.com"
  And I fill in "Password" with "123456"
  Then I press "Entrar"
  Then I click on an element with id of "user-link"
  Then I click on an element with id of "edituser"
  Then I click on an element with id of "deleteuser"
  And I should see an element with id of "enter-button"

Scenario: Test
	When I visit site page "/gustavo"
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I should see "Meus Dados"
	Then I click on an element with id of "deleteuser"
	And I should see an element with id of "enter-button"
