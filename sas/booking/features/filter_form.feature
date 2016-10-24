Feature: Search Bookings

Background:
  Given I run loaddata to populate dropdowns
  And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574" and category "Student"

Scenario: Filtering by Day x Room
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Day x Room"
  Then There should be exactly 2 elements matching $(":disabled")

Scenario: Filtering by Booking x Week
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Booking x Week"
  Then There should be exactly 2 elements matching $(":disabled")

Scenario: Filtering by Building x Day
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Building x Day"
  Then There should be exactly 3 elements matching $(":disabled")

Scenario: Filtering by Room x Period
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Room x Period"
  Then There should be exactly 1 elements matching $(":disabled")

Scenario: Selecting place according to building
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Room x Period"
  Then I select "UAC" from "Building:"
  Then I should not see option "UED" in selector "Place:"
