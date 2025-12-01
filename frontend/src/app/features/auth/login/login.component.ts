import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule],
    template: `
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="bg-white p-8 rounded shadow-md w-96">
        <h2 class="text-2xl font-bold mb-6 text-center">Connexion</h2>
        
        <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          
          <div class="mb-4">
            <label class="block text-gray-700">Nom d'utilisateur</label>
            <input formControlName="username" type="text" class="w-full mt-1 p-2 border rounded" placeholder="ethernanos">
          </div>

          <div class="mb-6">
            <label class="block text-gray-700">Mot de passe</label>
            <input formControlName="password" type="password" class="w-full mt-1 p-2 border rounded" placeholder="******">
          </div>

          <button 
            type="submit" 
            [disabled]="loginForm.invalid"
            class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            Se connecter
          </button>

        </form>

        <p *ngIf="error" class="mt-4 text-red-500 text-center text-sm">{{ error }}</p>
      </div>
    </div>
  `
})
export class LoginComponent {
    private fb = inject(FormBuilder);
    private auth = inject(AuthService);
    private router = inject(Router);

    error = '';

    loginForm = this.fb.group({
        username: ['', Validators.required],
        password: ['', Validators.required]
    });

    onSubmit() {
        if (this.loginForm.invalid) return;

        const { username, password } = this.loginForm.value;

        this.auth.login({ username: username!, password: password! }).subscribe({
            next: () => {
                // Redirection vers le tableau de bord après succès
                this.router.navigate(['/dashboard']);
            },
            error: (err: any) => {
                console.error(err);
                this.error = 'Identifiants incorrects ou serveur injoignable.';
            }
        });
    }
}