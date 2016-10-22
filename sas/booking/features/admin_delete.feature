Feature: Admin_Delete_Table

Background:
	Given I run loaddata to populate dropdowns


Scenario: Inexistent booking between start date and end date
	When I login in with email "fhc@planalto.gov.com" and password "123456"
	Then I visit site page "/booking/searchbooking/"
	Then I should see "Mostrando 0 até 0 de 0 registros"
