Feature: User Deleting a Booking

Background:
	Given I run loaddata to populate dropdowns
  And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574" and category "Student"
  And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-11-20" and end_date "2018-11-30" of user "lucas@gmail.com"

Scenario: Delete a booking successfully
	When I login in with email "lucas@gmail.com" and password "123456"
	Then I visit site page "/booking/searchbooking/"
	Then I should see an element with id of "delete-booking"
  Then I click on an element with id of "delete-booking"
  And I should see "Are you sure you want to delete this booking?"
  Then I click on an element with id of "action-delete"
  Then I should not see an element with id of "delete-booking"
