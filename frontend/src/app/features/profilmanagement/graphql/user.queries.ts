import { gql } from 'apollo-angular';

export const GET_ALL_USERS = gql`
  # Le nom "GetAllUsers" sera utilisé dans l'URL !
  query users {
    users {
      id
      username
      email
      firstName
      lastName
      isActive
      dateJoined
      roles {
        name
      }
    }
  }
`;