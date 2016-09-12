Feature: Login

Scenario: User alredy registered
  And I register the user "lucas" with the password "123456"
  When I visit site page "/user/login"
  And I fill in "Username" with "lucas"
  And I fill in "Password" with "123456"
  Then I press "Enviar"
  Then I should see "Parabéns você está logado!!"
