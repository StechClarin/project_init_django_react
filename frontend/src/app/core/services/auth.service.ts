import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

// Interface pour la réponse Django
interface AuthResponse {
  access: string;
  refresh: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private apiUrl = environment.apiUrl; // ex: http://127.0.0.1:8000/api

  // Signal pour savoir si on est connecté
  currentUserSignal = signal(this.hasToken());

  // --- LOGIN ---
  login(credentials: {username: string, password: string}) {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login/`, credentials).pipe(
      tap(response => {
        // 1. On stocke les tokens
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        
        // 2. On met à jour le signal
        this.currentUserSignal.set(true);
      })
    );
  }

  // --- LOGOUT ---
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.currentUserSignal.set(false);
    this.router.navigate(['/login']);
  }

  // --- UTILITAIRES ---
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private hasToken(): boolean {
    return !!localStorage.getItem('access_token');
  }
}