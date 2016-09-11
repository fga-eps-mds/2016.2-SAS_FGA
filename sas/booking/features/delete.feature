Feature: Delete

Scenario: User already registered and wants to delete their account
  When I visit site page "/user/listuser"
  And I press "Deletar conta"
  Then I am redirected to "/user/deleteUser"
  Then I press "Deletar"
  Then I should see "Usuário deletado com sucesso!"
