Feature: Admin Pending Bookings

Background:
	Given I register an admin with email "teste123@email.com" and password "123456" and registration number "160000000" and category "Student"
	And I register the booking "Quimica" with the building "UED" with the place name "FGA-LAB_QUIMICA" and start_date "2020-11-20" and end_date "2020-11-30" of user "teste123@email.com"
	And I register the booking "Quimica 2" with the building "UED" with the place name "FGA-LAB_QUIMICA" and start_date "2021-11-20" and end_date "2021-11-30" of user "teste123@email.com"

Scenario: Admin View Pending Bookings
	When I login in with email "teste123@email.com" and password "123456" 
	And I visit site page "/booking/pendingbookings/"
	And I should see "Quimica"
	Then I should see "Quimica 2"

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
