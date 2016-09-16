Feature: Login

Background: 
	Given I register the user "lucas@gmail.com" with the password "123456"

Scenario: Login successfully
	When I visit site page "/"
	Then I should see an element with id of "enter-button"	
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "lucas@gmail.com"
	And I fill in "Password" with "123456"
	Then I press "Entrar"
	Then I should see "Hi, Pudim"

Scenario: Wrong password
	When I visit site page "/"
	Then I should see an element with id of "enter-button"	
	Then I click on an element with id of "enter-button"
	And I type in "lucas12@gmail.com" to "Email"
	And I type in "Password" to "Password"
	Then I press "Entrar"
	Then I should see "Email or Password does not match"

Scenario: Wrong email
	When I visit site page "/"
	Then I should see an element with id of "enter-button"	
	Then I click on an element with id of "enter-button"
	And I type in "luc12@gmail.com" to "Email"
	And I type in "123456" to "Password"
	Then I press "Entrar"
	Then I should see "Email or Password does not match"
