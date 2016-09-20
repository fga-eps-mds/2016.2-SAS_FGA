Feature: EditUser

Background:
	Given I register the user "lucas@gmail.com" with the password "123456"

Scenario: User registered
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Name" with "Pedro Pereira Pinto"
	And I press "Salvar Dados"
	Then I should see "Your data has been updated"

Scenario: User empties one field
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Email" with ""
	And I press "Salvar Dados"
	Then I should see an alert with text "Please fill out this field."

Scenario: Duplicated email
	When I register the user "pedrot@gmail.com" with the password "123456"
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Email" with "pedrot@gmail.com"
	And I press "Salvar Dados"
	Then I should see "Email already used"

Scenario: Actual password wrong
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I click on an element with id of "changepassword"
	And I should see an element with id of "id_password"
	And I type in "12345fjksj" to "Password"  
	And I type in "asdfgh" to "New Password" 
	And I type in "asdfgh" to id "renew_password" 
	And I press "Alterar senha"
	Then I should see "Password is wrong"

Scenario: Change password successfully
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I click on an element with id of "changepassword"
	And I should see an element with id of "id_password"
	And I type in "123456" to "Password"  
	And I type in "asdfgh" to "New Password" 
	And I type in "asdfgh" to id "renew_password" 
	And I press "Alterar senha"
	Then I should see "Your password has been changed"

Scenario: New Password do not match
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I click on an element with id of "changepassword"
	And I should see an element with id of "id_password"
	And I type in "123456" to "Password"  
	And I type in "asdfgh" to "New Password" 
	And I type in "asdfgh3iu4i3" to id "renew_password" 
	And I press "Alterar senha"
	Then I should see "Passwords do not match"
