Feature: table_booking

Background:
	Given I run loaddata to populate dropdowns
	And I load a semester
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-10-20" and end_date "2018-10-30" of user "lucas@gmail.com"

Scenario: Successfully booking creation
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "10/20/2018"
    And I fill in "Date (To)" with "10/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
    Then I click on an element with id of "create-booking"
    And I fill in "Booking Name" with "reuniao"
    Then I click on an element with id of "action-create"
    Then I click on an element with id of "button-confirm"
    Then I should see "Booking has been saved."

Scenario: canceling a book
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "10/20/2018"
    And I fill in "Date (To)" with "10/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
    Then I click on an element with id of "create-booking"
    And I fill in "Booking Name" with "reuniao"
    Then I click on an element with id of "action-create"
    Then I click on an element with id of "button-cancel"
    Then I should see "Booking has been canceled"

Scenario: modal receives correct data
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room "
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Date:" with "10/20/2018"
    And I fill in "Date (To)" with "10/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
    Then I click on an element with id of "create-booking"
    And I fill in "Booking Name" with "reuniao"
    Then I click on an element with id of "action-create"
    Then I should see "FGA-I1"
    Then I should see "reuniao"
    Then I should see "Oct. 20, 2018"
    Then I should see "6 a.m."
    Then I should see "8 a.m."
