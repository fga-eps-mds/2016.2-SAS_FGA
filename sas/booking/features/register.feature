Feature: Register

Scenario: User not registered
  When I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Register"
  Then I should see "You have been registered"

Scenario: User do not inform Registration Number
  When I visit site page "/user/newuser"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Register"
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
  Then I press "Register"
  Then I should see "Email already used"

Scenario: Repeated Registration Number
  When I register the user "test123@gmail.com" with the password "123456" and with registration_number "100200300"
  And I visit site page "/user/newuser"
  And I type in "100200300" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Register"
  Then I should see an alert with text "Registration Number already used"

Scenario: User do not inform Email
  When I register the user "test123@gmail.com" with the password "123456"
  And I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Register"
  Then I should see an alert with text "Please fill out this field."

Scenario: User Informed an Invalid Email
  When I register the user "sender" with the password "123456"
  And I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "sender"
  And I type in "teste123" to "Password"
  And I type in "teste123" to "Repeat Password"
  Then I press "Register"
  Then I should see an alert with text "Invalid Email, user was not registered"

Scenario: User do not Inform Password
  When I register the user "test123@gmail.com" with the password "123456"
  And I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Repeat Password"
  Then I press "Register"
  Then I should see an alert with text "Please fill out this field."

Scenario: User do not Inform Repeat Password
  When I register the user "test123@gmail.com" with the password "123456"
  And I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  Then I press "Register"
  Then I should see an alert with text "Please fill out this field."

Scenario: User Informs Different Password and Repeat Password fields
  When I register the user "test123@gmail.com" with the password "123456"
  And I visit site page "/user/newuser"
  And I type in "120030559" to "Registration Number"
  And I select "Student" from "Category"
  And I fill in "Name" with "Pedro Pereira Pinto"
  And I fill in "Email" with "pedropp@gmail.com"
  And I type in "teste123" to "Password"
  And I type in "123teste" to "Repeat Password"
  Then I press "Register"
  Then I should see an alert with text "Password and Repeat Password fields dont match"

