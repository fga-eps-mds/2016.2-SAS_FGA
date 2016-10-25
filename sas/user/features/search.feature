Feature: Search Users

Background:
  Given I run loaddata to populate dropdowns
  And I register an admin with email "carlarocha@email.com" and password "123456" and registration number "150003256" and category "Teaching Staff"

Scenario: View not admin users
    When I register the user "luis@gmail.com" with the password "123456" and registration number "140016574" and category "Student"
	When I login in with email "carlarocha@email.com" and password "123456"
	Then I visit site page "/user/searchuser/"
	Then I should see "140016574"

Scenario: No registered user
	When I login in with email "carlarocha@email.com" and password "123456"
    Then I visit site page "/user/searchuser/"
    Then I should not see an element with id of "make-an-admin"

Scenario: All registered user are admin
	When I register an admin with email "paulomeireles@email.com" and password "123456" and registration number "150007894" and category "Teaching Staff"
	When I login in with email "carlarocha@email.com" and password "123456"
    Then I visit site page "/user/searchuser/"
	Then I should see "150007894"
    Then I should not see an element with id of "make-an-admin"
