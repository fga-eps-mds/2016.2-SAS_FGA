Feature: Register

Scenario: User not registered
  When I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Cadastrar"
  Then I should see "Entrar"

Scenario: User do not inform Registration Number
  When I visit site page "/user/newuser"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Cadastrar"
  Then I should see "Entrar"
  Then I should see an alert with text "Please fill out this field."

Scenario: Repeated Email
	When I register the user "test123@gmail.com" with the password "123456"
	And I visit site page "/user/newuser"
	And I type in "120030559" to "Registration Number"
	And I select "Student" from "Category"
	And I fill in "Name" with "Pedro Pereira Pinto"
	And I fill in "Email" with "test123@gmail.com"
	And I type in "teste123" to "Password"
	And I type in "teste123" to "Repeat Password"
	Then I press "Cadastrar"
	Then I should see "Entrar"
	Then I should see "Email already used"
