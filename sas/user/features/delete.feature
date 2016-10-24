Feature: Delete

Background:
  Given I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574" and category "Student"

Scenario: Test
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/edituser/"
	And I should see "Personal Data"
	Then I click on an element with id of "deleteuser"
	And I should see an element with id of "enter-button"
