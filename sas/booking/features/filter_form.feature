Feature: Search Bookings

Background:
  Given I run loaddata to populate dropdowns
  And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"

Scenario: Filtering by Day x Room
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Room's Week Timetable"
  Then I should see "Building"
  And I should see "Place"
  And I should see "Date"

Scenario: Filtering by Booking x Week
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Booking"
  Then I should see "Booking"
  And I should see "Date"
  And I should see "Date (To)"

Scenario: Filtering by Building x Day
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Occupation"
  Then I should see "Building"
  And I should see "Date"

Scenario: Filtering by Room x Period
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Room"
  Then I should see "Building"
  And I should see "Place"
  And I should see "Date"
  And I should see "Date (To)"

Scenario: Selecting place according to building
  When I login in with email "lucas@gmail.com" and password "123456"
  Then I visit site page "/booking/searchbookingg/"
  Then I choose "Room"
  Then I select "UAC" from "Building:"
  Then I should not see option "UED" in selector "Place:"
