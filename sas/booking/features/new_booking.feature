Feature: New Booking 

Background:
    Given I run loaddata to populate dropdowns
    And I load a semester
    And I register an admin with email "lucas@gmail.com" and password "123456" and registration number "140016574" and category "Teaching Staff"
    And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-10-20" and end_date "2018-10-30" of user "lucas@gmail.com"

Scenario: Sucessfull Booking creation 
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/newbooking/"
    And I fill in "Booking Name:" with "Teste"
    And I choose "No"
    And I fill in "Start Date:" with "10/20/2019"
    And I fill in "End Date:" with "10/30/2019"
    And I select "UAC" from "Building"
    And I select "UAC | FGA-I1" from "Place"
    And I select "20:00" from "Start Time:"
    And I select "22:00" from "End Time:"
    And I click on an element with id of "id_week_days_0"
    Then I press "Perform Booking"
    Then I should see "Confirm"
