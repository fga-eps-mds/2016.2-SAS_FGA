Feature: Register

Scenario: User not registered
  When I visit site page "/user/newuser"
  And I type in "12/0030559" to "Registration Number"
  And I select "Aluno" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Username" with "pedropp"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Enviar"
  Then I should see "Welcome to SAS"


