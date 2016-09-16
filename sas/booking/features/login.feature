Feature: Login

Background: 
	Given I register the user "lucas@gmail.com" with the password "123456"

Scenario: Login successfully
	When I visit site page "/"
	Then I should see an element with id of "enter-button"	
	Then I click on an element with id of "enter-button"
	And I fill in "Username" with "lucas@gmail.com"
	And I fill in "Password" with "123456"
	Then I press "Entrar"
	Then I should see "Hi, Pudim"

Scenario: Wrong user
	When I visit site page "/"
	Then I should see an element with id of "enter-button"	
	Then I click on an element with id of "enter-button"
	And I fill in "Username" with "lucas12@gmail.com"
	And I fill in "Password" with "123456"
	Then I press "Entrar"
	Then I should see "Hi, Pudim"
