Feature: Delete

Background:
  Given I register the user "lucas@gmail.com" with the password "123456"

Scenario: Test
	When I visit site page "/gustavo"
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I should see "Meus Dados"
	Then I click on an element with id of "deleteuser"
	And I should see an element with id of "enter-button"
