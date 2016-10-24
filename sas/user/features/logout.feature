Feature: LogoutUser

Background:
	Given I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574" and category "Student"

Scenario: User registered
	When I login in with email "lucas@gmail.com" and password "123456"
	And I visit site page "/user/logout/"
  Then I should see "You have been logged out successfully!"

Scenario: User not registered
  When I visit site page "/user/logout/"
  Then I should not see "You have been logged out successfully!"
