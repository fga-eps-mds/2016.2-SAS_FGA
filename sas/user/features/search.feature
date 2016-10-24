Feature: Search Users

Background:
  Given I run loaddata to populate dropdowns
  And I register the user "lucas@email.com" with the password "123456" and registration number "150016234"
  And This user with email "lucas@email.com" is an admin

Scenario: View users
    When I register the user "luis@gmail.com" with the password "123456" and registration number "140016574"
	When I login in with email "lucas@email.com" and password "123456"
	Then I visit site page "/user/searchuser/"
	Then I should see "140016574"
