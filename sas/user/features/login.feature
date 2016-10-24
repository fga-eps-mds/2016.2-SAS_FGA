Feature: Login

Background:
	Given I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574" and category "Student"

Scenario: Login successfully
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "lucas@gmail.com"
	And I fill in "Password" with "123456"
	Then I press "Sign In"
	Then I should see "Hi, Usuário"

Scenario: User does not exist
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "leticia@hotmail.com"
	And I fill in "Password" with "lelepass"
	Then I press "Sign In"
	Then I should see "Email or Password does not match"

Scenario: Login without email
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with ""
	And I fill in "Password" with "123456"
	Then I press "Sign In"
	Then I should see an alert with text "Please fill out this field."

Scenario: Wrong password
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "lucas@gmail.com"
	And I fill in "Password" with "password"
	Then I press "Sign In"
	Then I should see "Email or Password does not match"

	Scenario: Login without email
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "lucas@gmail.com"
	And I fill in "Password" with ""
	Then I press "Sign In"
	Then I should see an alert with text "Please fill out this field."

Scenario: Wrong email
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "fernando@email.com"
	And I fill in "Password" with "123456"
	Then I press "Sign In"
	Then I should see "Email or Password does not match"

Scenario: Registered email with wrong password
	When I visit site page "/"
	Then I should see an element with id of "enter-button"
	Then I click on an element with id of "enter-button"
	And I fill in "Email" with "lucas@gmail.com"
	And I fill in "Password" with "456123"
	Then I press "Sign In"
	Then I should see "Email or Password does not match"
