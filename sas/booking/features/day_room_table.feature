Feature: Day_Room_Table

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-12-20" and end_date "2018-12-30" of user "lucas@gmail.com"


Scenario: Inexistent booking in the specified room
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room's Week Timetable"
    And I select "UED" from "Building"
    And I select "UED | FGA-LAB_MATERIAIS" from "Place"
    And I fill in "Date:" with "12/21/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"

Scenario: Inexistent booking on the specified day
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room's Week Timetable"
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "12/19/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
