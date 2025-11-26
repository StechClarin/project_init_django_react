import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { AuthResponse, User } from '../../features/profilmanagement/models/user.model';

@Injectable({
  providedIn: 'root' // Singleton: accessible partout
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl; // http://127.0.0.1:8000/api

  // Signal: La façon moderne de gérer l'état "Est connecté ?"
  // (Plus simple que NgRx pour juste un booléen)
  currentUser = signal<User | null>(null);

  constructor() {
    // TODO: Au démarrage, on pourrait vérifier si un token existe déjà
    // et recharger le user. Pour l'instant, on commence vide.
  }

  login(credentials: {username: string, password: string}) {
    // 1. Appel à Django (POST /api/auth/login/)
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login/`, credentials)
      .pipe(
        tap(response => {
          // 2. Succès ! On stocke les tokens
          this.saveTokens(response);
          
          // 3. (Optionnel pour l'instant) On pourrait décoder le token 
          // pour mettre à jour currentUser. On fera ça plus tard.
          console.log('🔑 Connexion réussie ! Token:', response.access);
        })
      );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.currentUser.set(null);
  }

  // --- Gestion des Tokens ---

  private saveTokens(tokens: AuthResponse) {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }
}