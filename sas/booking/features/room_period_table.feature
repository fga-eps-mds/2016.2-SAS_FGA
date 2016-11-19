Feature: Room_Period_Table

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-11-20" and end_date "2018-11-30" of user "lucas@gmail.com"

Scenario: Inexistent booking in the specified room
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UED" from "Building"
    And I select "UED | FGA-LAB_MATERIAIS" from "Place"
    And I fill in "Date:" with "11/21/2018"
    And I fill in "Date (To)" with "12/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"

Scenario: Inexistent booking between end date and start date
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "11/21/2018"
    And I fill in "Date (To)" with "12/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"

Scenario: Start date lower than actual date
	When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
	And I select "UAC" from "Building"
	And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "10/10/2015"
    And I fill in "Date (To)" with "12/30/2018"
    Then I press "Search"
    Then I should see "Invalid booking period: Booking must be in future date"

Scenario: End date lower than actual date
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "12/30/2020"
    And I fill in "Date (To)" with "10/10/2015"
    Then I press "Search"
    Then I should see "Invalid booking period: Booking must be in future date"

Scenario: Start Date greater then End Date
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "12/31/2020"
    And I fill in "Date (To)" with "12/30/2018"
    Then I press "Search"
    Then I should see "End date must be equal or greater then Start date"
