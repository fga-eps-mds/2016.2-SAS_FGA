Feature: EditUser

Background:
	Given I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574" and category "Student"

Scenario: Invalid email
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Email" with "pedro"
	And I select "Student" from "Category"
	And I press "Save Data"
	Then I should see "Email address must be in a valid format."

Scenario: User registered
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Name" with "Pedro Pereira Pinto"
	And I select "Student" from "Category"
	And I press "Save Data"
	Then I should see "Your data has been updated"

Scenario: User empties email
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Email" with ""
	And I press "Save Data"
	Then I should see an alert with text "Please fill out this field."

Scenario: User empties name
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Name" with ""
	And I press "Save Data"
	Then I should see an alert with text "Please fill out this field."

Scenario: User empties registration number
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Registration number" with ""
	And I press "Save Data"
	Then I should see an alert with text "Please fill out this field."

Scenario: User empties category
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I select "----" from "Category"
	And I press "Save Data"
	Then I should see an alert with text "Please select an item on the list."

Scenario: Duplicated email
	When I register the user "pedro@gmail.com" with the password "123456" and registration number "150016572" and category "Student"
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I fill in "Email" with "pedro@gmail.com"
	And I select "Student" from "Category"
	And I press "Save Data"
	Then I should see "Email already used"

Scenario: Actual password wrong
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I click on an element with id of "changepassword"
	And I should see an element with id of "id_password"
	And I type in "12345fjksj" to "Password"
	And I type in "asdfgh" to "New Password"
	And I type in "asdfgh" to id "renew_password"
	And I press "Change Password"
	Then I should see "Current password is wrong"

Scenario: Change password successfully
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I click on an element with id of "changepassword"
	And I should see an element with id of "id_password"
	And I type in "123456" to "Password"
	And I type in "asdfgh" to "New Password"
	And I type in "asdfgh" to id "renew_password"
	And I press "Change Password"
	Then I should see "Your password has been changed"

Scenario: New Password do not match
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I click on an element with id of "changepassword"
	And I should see an element with id of "id_password"
	And I type in "123456" to "Password"
	And I type in "asdfgh" to "New Password"
	And I type in "asdfgh3iu4i3" to id "renew_password"
	And I press "Change Password"
	Then I should see "Passwords do not match"
