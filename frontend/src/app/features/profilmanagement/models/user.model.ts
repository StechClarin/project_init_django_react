export interface User {
  id: string;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  isActive: boolean;
  dateJoined: string;
  role?: {
    id: string;
    name: string;
  };
}