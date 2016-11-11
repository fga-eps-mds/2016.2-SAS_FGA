Feature: Building_Day_Table

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-11-20" and end_date "2018-11-30" of user "lucas@gmail.com"


Scenario: No booking in the building
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Occupation"
    And I select "UED" from "Building"
    And I fill in "Date:" with "11/21/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"

Scenario: No booking in the day
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Occupation"
    And I select "UAC" from "Building"
    And I fill in "Date:" with "11/19/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
