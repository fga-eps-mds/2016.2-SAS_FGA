Feature: Responsible_Table

Background:
	Given I run loaddata to populate dropdowns
	And I register the user "lucas@gmail.com" with the password "123456" and registration number "140016574"
	And I register the booking "monitoria" with the building "UAC" with the place name "FGA-I1" and start_date "2018-11-20" and end_date "2018-11-30" of responsible "lucas@gmail.com"

Scenario: All fields correct
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Responsible"
    And I fill in "Date:" with "11/21/2018"
    And I select "lucas@gmail.com" from "Responsible"
    Then I press "Search"
    Then I should see "Responsible"

Scenario: No booking in the day
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Responsible"
    And I fill in "Date:" with "11/21/2020"
    And I select "lucas@gmail.com" from "Responsible"
    Then I press "Search"
    Then I should see "Invalid option"

Scenario: No day select
    When I login in with email "lucas@gmail.com" and password "123456"
    Then I visit site page "/booking/searchbookingg/"
    And I choose "Responsible"
    And I select "lucas@gmail.com" from "Responsible"
    Then I press "Search"
    Then I should see an alert with text "Please fill out this field."