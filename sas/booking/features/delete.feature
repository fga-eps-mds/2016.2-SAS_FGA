Feature: Delete

Background:
  Given I register the user "lucas@email.com" with the password "123456"
  When I visit site page "/"
  Then I should see an element with id of "enter-button"
  Then I click on an element with id of "enter-button"
  And I fill in "Email" with "lucas@email.com"
  And I fill in "Password" with "123456"
  Then I press "Entrar"

Scenario: User already registered and wants to delete their account
  Then I should see an element with id of "user-link"
  Then I click on an element with id of "user-link"
  Then I should see "Meus Dados" on an element "li"
  And I click on an element "li" called "Meus Dados"
  And I press "Excluir minha conta"
  Then I am redirected to "/user/deleteUser"
