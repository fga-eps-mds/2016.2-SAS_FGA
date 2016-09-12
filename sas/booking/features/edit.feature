Feature: Edit

Scenario: User registered
  When I visit site page "/user/edituser/1"
  And I fill in "Name" with "Pedro Silva"
  And I fill in "Username" with "pedra1"
  And I fill in "Email" with "pedra@gmail.com"
  And I type in "teste123" to "Password"	
  And I type in "teste1234" to "Password"
  And I type in "teste1234" to "Repeat Password"
  Then I press "Editar"
  Then I should see "Listing User"