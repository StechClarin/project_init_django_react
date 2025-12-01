import { gql } from 'apollo-angular';

export const GET_SIDEBAR_MODULES = gql`
  query {
    modules {
      id
      name
      icon
      pages {
        id
        title
        icon
        link
      }
    }
  }
`;
