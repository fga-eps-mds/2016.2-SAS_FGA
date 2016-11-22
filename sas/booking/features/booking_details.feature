Feature: Booking Details

Background:
	Given I run loaddata to populate dropdowns
	And I load a semester
	And I register an admin with email "teste123@email.com" and password "123456" and registration number "160000000" and category "Teaching Staff"


Scenario: Viewing details of booking
	When I login in with email "teste123@email.com" and password "123456"
	And I register the booking "Eletricidade" with the building "UED" with the place name "FGA-LAB_ELETRICIDADE" and start_date "2016-11-20" and end_date "2016-11-30" of user "teste123@email.com"
	And I visit site page "/booking/searchbooking/"
	And I should see "Eletricidade"
        Then I should see an element with id of "booking-details"
        Then I click on an element with id of "booking-details"
        Then I should see "Eletricidade"

Scenario: Viewing details of tagged booking
	When I login in with email "teste123@email.com" and password "123456"
	And I register the tagged booking "Eletricidade" with the building "UED" with the place name "FGA-LAB_ELETRICIDADE" and start_date "2016-11-20" and end_date "2016-11-30" of user "teste123@email.com" and tag "Tagging"
	And I visit site page "/booking/searchbooking/"
	And I should see "Eletricidade"
        Then I should see an element with id of "booking-details"
        Then I click on an element with id of "booking-details"
        Then I should see "Tagging"
