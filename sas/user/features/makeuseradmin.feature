Feature: Admin make an User an Admin

Background:
    Given I run loaddata to populate dropdowns
  And I register an admin with email "lucas@gmail.com" and password "123456" and registration number "140016574" and category "Teaching Staff"

Scenario: Make an user an admin
    When I register the user "usuario@gmail.com" with the password "1234567" and registration number "140017815" and category "Student"
	Then I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/searchuser/"
  Then I should see an element with id of "make-an-admin"
  Then I click on an element with id of "make-an-admin"
  And I should see "Are you sure you want to make this user an admin?"
  Then I click on an element with id of "action-make-admin"
  Then I should not see an element with id of "make-an-admin"

Scenario: All users are admins
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/user/searchuser/"
    Then I should not see an element with id of "make-an-admin"
