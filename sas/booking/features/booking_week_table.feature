Feature: Booking_Week_Table

Background:
    Given I run loaddata to populate dropdowns
    And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"

Scenario: Booking is not between date and date to
    When I login in with email "lucas@gmail.com" and password "123456"
    When I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-12-20" and end_date "2018-12-30" of user "lucas@gmail.com"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking"
    And I fill in "Date:" with "12/10/2018"
    And I fill in "Date (To):" with "12/30/2018"
    And I select "monitoria" from "Booking:"
    Then I press "Search"
    Then I should see an element with id of "create-booking"

Scenario: No booking created
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking"
    And I fill in "Date:" with "12/10/2018"
    And I fill in "Date (To):" with "12/30/2018"
    Then I press "Search"
    Then I should see an alert with text "Please select an item in the list."
