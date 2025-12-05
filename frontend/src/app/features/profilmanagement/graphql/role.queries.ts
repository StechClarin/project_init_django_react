import { gql } from 'apollo-angular';

export const GET_ALL_ROLES = gql`
  query roles {
    roles {
      id
      name
    }
  }
`;
