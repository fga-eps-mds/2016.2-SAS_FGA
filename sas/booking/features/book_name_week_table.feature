Feature: Booking_Week_Table

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2016-12-21" and end_date "2016-12-30" of user "lucas@gmail.com"

Scenario: Inexistent booking between start date and end date
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/booking/searchbookingg/"
	And I choose "Booking x Week"
    And I fill in "Booking Name" with "monitoria"
	And I fill in "Start Date" with "12/10/2016"
	And I fill in "End Date" with "12/15/2016"
	Then I press "Search"
	Then I should see "Doesnt exist any booking in this period of time"

Scenario: Inexistent booking in the specified name
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking x Week"
    And I fill in "Booking Name" with "monitoria"
    And I fill in "Start Date" with "12/10/2016"
    And I fill in "End Date" with "12/15/2016"
    Then I press "Search"
    Then I should see "Doesnt exist any booking with this name"

Scenario: Start date lower than actual date
	When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking x Week"
    And I fill in "Booking Name" with "monitoria"
    And I fill in "Start Date" with "12/10/2016"
    And I fill in "End Date" with "12/15/2016"
    Then I press "Search"
    Then I should see "Start date must be from future date"

Scenario: End date lower than actual date
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking x Week"
    And I fill in "Booking Name" with "monitoria"
    And I fill in "Start Date" with "12/10/2016"
    And I fill in "End Date" with "12/15/2016"
    Then I press "Search"
    Then I should see "End date must be from future date"

Scenario: Start Date greater then End Date
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking x Week"
    And I fill in "Booking Name" with "monitoria"
    And I fill in "Start Date" with "12/10/2016"
    And I fill in "End Date" with "12/15/2016"
    Then I press "Search"
    Then I should see "End date must be equal or greater then Start date"

Scenario: All valid inputs
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Booking x Week"
    And I fill in "Booking Name" with "monitoria"
    And I fill in "Start Date" with "12/10/2016"
    And I fill in "End Date" with "12/15/2016"
    Then I press "Search"
    Then I should see "FGA-I1"