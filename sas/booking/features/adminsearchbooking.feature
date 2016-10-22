Feature: Admin View Booking

Scenario: Admin View
    When I create bookings
    When I login in with email "fhc@planalto.gov.com" and password "123456" 
    And I visit site page "/booking/allbookings/"
   And I should see "Teste Michel"
    And I should see "Teste Fhc"
    And I should see "Teste Test"

 Scenario: Academic Staff View
    When I create bookings
    When I login in with email "test@test.com" and password "123456" 
    And I visit site page "/booking/searchbooking/"
    And I should see "Teste Test" 
