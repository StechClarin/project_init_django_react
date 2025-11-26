export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role?: string; // Ou un objet Role si ton API renvoie un objet
}

// La réponse de Django SimpleJWT quand on se connecte
export interface AuthResponse {
  access: string;  // Le token d'accès (courte durée)
  refresh: string; // Le token de rafraîchissement (longue durée)
}