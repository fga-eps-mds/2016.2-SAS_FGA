Feature: Room_Period_Table

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2016-11-20" and end_date "2016-11-30"

Scenario: Inexistent booking between start date and end date
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/booking/searchbookingg/"
	And I choose "Room x Period"
	And I select "UAC" from "Building"
	And I select "UAC | FGA-I1"
	And I fill in "Start Date" with "10/20/2016"
	And I fill in "End Date" with "10/30/2016"
	Then I should see "Doesnt exist any booking in this period of time"
