Feature: Settings

Background:
       Given I register an admin with email "lucas@gmail.com" and password "123456" and registration number "140016574" and category "Teaching Staff"

Scenario: Admin register a semester
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/settings/"
        And I fill in "Semester Start:" with "10/20/2017"
        And I fill in "Semester End:" with "10/20/2018"
        Then I press "Register"
        Then I should see "Settings updated"


Scenario: Invalid semester inputs
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/user/settings/"
        And I fill in "Semester Start:" with "10/20/2017"
        And I fill in "Semester End:" with "10/20/2010"
        Then I press "Register"
        Then I should see "Semester start must be before the end of it."
