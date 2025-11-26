// Fichier: src/app/features/auth/login/login.component.ts
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '@app/core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule], // On importe les modules nécessaires
  template: `
    <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl">
        
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Connexion Giga-Projet
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Connectez-vous pour accéder à l'admin
          </p>
        </div>

        <form class="mt-8 space-y-6" [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          
          <div *ngIf="errorMessage()" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
            {{ errorMessage() }}
          </div>

          <div class="rounded-md shadow-sm -space-y-px">
            
            <div class="mb-4">
              <label for="username" class="sr-only">Nom d'utilisateur</label>
              <input 
                id="username" 
                type="text" 
                formControlName="username" 
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
                placeholder="Nom d'utilisateur (ex: ethernanos)"
              >
              <span *ngIf="loginForm.get('username')?.touched && loginForm.get('username')?.invalid" class="text-red-500 text-xs">
                Le nom d'utilisateur est requis.
              </span>
            </div>

            <div class="mb-4">
              <label for="password" class="sr-only">Mot de passe</label>
              <input 
                id="password" 
                type="password" 
                formControlName="password" 
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
                placeholder="Mot de passe"
              >
              <span *ngIf="loginForm.get('password')?.touched && loginForm.get('password')?.invalid" class="text-red-500 text-xs">
                Le mot de passe est requis.
              </span>
            </div>
          </div>

          <div>
            <button 
              type="submit" 
              [disabled]="loginForm.invalid || isLoading()"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span *ngIf="isLoading()">Chargement...</span>
              <span *ngIf="!isLoading()">Se connecter</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  `
})
export class LoginComponent {
  // Injection des dépendances (Style moderne Angular 16+)
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  // État local (Signals)
  isLoading = signal(false);
  errorMessage = signal<string | null>(null);

  // Le Formulaire
  loginForm = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.isLoading.set(true);
    this.errorMessage.set(null);

    const credentials = {
      username: this.loginForm.value.username!,
      password: this.loginForm.value.password!
    };

    this.authService.login(credentials).subscribe({
      next: () => {
        // Succès : Redirection vers la page d'accueil (ou dashboard)
        this.isLoading.set(false);
        this.router.navigate(['/']); 
      },
      error: (err) => {
        // Erreur : On affiche le message
        console.error('Erreur login:', err);
        this.isLoading.set(false);
        this.errorMessage.set("Nom d'utilisateur ou mot de passe incorrect.");
      }
    });
  }
}
