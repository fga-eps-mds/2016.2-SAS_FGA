Feature: Admin Pending Bookings

Background:
	Given I run loaddata to populate dropdowns
	And I load a semester
	And I register an admin with email "teste123@email.com" and password "123456" and registration number "160000000" and category "Teaching Staff"
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "Eletricidade" with the building "UED" with the place name "FGA-LAB_ELETRICIDADE" and start_date "2016-11-20" and end_date "2016-11-30" of user "lucas@gmail.com"

Scenario: Admin View Pending Bookings
	When I login in with email "teste123@email.com" and password "123456"
	And I visit site page "/booking/pendingbookings/"
	And I should see "Eletricidade"

Scenario: Admin approve bookings
	When I login in with email "teste123@email.com" and password "123456"
	And I visit site page "/booking/pendingbookings/"
	And I should see an element with id of "approve-booking"
 	And I click on an element with id of "approve-booking"
	Then I should see "Booking Approved!"

Scenario: Admin denies bookings
	When I login in with email "teste123@email.com" and password "123456"
	And I visit site page "/booking/pendingbookings/"
	Then I should see an element with id of "deny-booking"
 	Then I click on an element with id of "deny-booking"
	Then I should see "Booking Denied!"
