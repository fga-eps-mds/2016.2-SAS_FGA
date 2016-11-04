Feature: table_booking

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-10-20" and end_date "2018-10-30" of user "lucas@gmail.com"

Scenario: Successfully booking creation
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room x Period"
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Start Date" with "10/20/2018"
    And I fill in "End Date" with "10/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
    Then I click on an element with id of "create-booking"
    And I fill in "Booking Name" with "reuniao"
    Then I click on an element with id of "action-create"
    #Then I should see "Mensagem de exito"

Scenario: Modal receives correct booking data
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Room x Period"
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I fill in "Start Date" with "10/20/2018"
    And I fill in "End Date" with "10/30/2018"
    Then I press "Search"
    Then I should see an element with id of "create-booking"
    Then I click on an element with id of "create-booking"
    Then I should see "FGA-I1"
