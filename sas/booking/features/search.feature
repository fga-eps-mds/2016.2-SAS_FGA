Feature: searchBooking

Background:
	Given I register the booking "Sleep" in the the place "UAC | FGA-S9"

Scenario: Invalid booking name
	When I visit site page "/booking/searchbookingquery"
	And I select "Booking x Week" from "Search options"
	And I fill in "Booking Name" with "Sleeep"
	And I fill in "Start Date" with "12/12/2016"
	And I press "Search"
	Then I should see "Doesnt exist any booking with this name"

Scenario: Invalid place
	When I visit site page "/booking/searchbookingquery"
	And I select "Room x Period" from "Search options"
	And I select "---------" from "Place"
	And I fill in "End Date" with "12/12/2016"
	And I press "Search"
	Then I should see "Inputs are in invalid format"

Scenario: Invalid building
	When I visit site page "/booking/searchbookingquery"
	And I select "Building x Day" from "Search options"
	And I select "---------" from "Building"
	And I fill in "Start Date" with "12/12/2016"
	And I press "Search"
	Then I should see "Inputs are in invalid format"
	
Scenario: Invalid start date
	When I visit site page "/booking/searchbookingquery"
	And I select "Booking x Week" from "Search options"
	And I fill in "Booking Name" with "Sleep"
	And I fill in "Start Date" with "2016/12/12"
	And I press "Search"
	Then I should see "Enter a valid date."

Scenario: Invalid end date
	When I visit site page "/booking/searchbookingquery"
	And I select "Room x Period" from "Search options"
	And I select "UAC | FGA-S9" from "Place"
	And I fill in "End Date" with "2016/12/12"
	And I press "Search"
	Then I should see "Enter a valid date."