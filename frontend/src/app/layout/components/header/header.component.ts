import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

// ✅ CORRECTION : Import propre via l'alias @core
import { AuthService } from '@core/services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  template: `
    <header class="h-16 bg-white shadow-sm border-b border-gray-200 flex items-center justify-between px-6 fixed top-0 right-0 left-64 z-40">
      <h1 class="text-xl font-semibold text-gray-800">Administration</h1>
      <div class="flex items-center space-x-4">
        <div class="text-right hidden sm:block">
          <p class="text-sm font-medium text-gray-900">EtherNanos</p>
          <p class="text-xs text-gray-500">Super Admin</p>
        </div>
        <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold border border-indigo-200">
          EN
        </div>
        <button (click)="logout()" class="p-2 text-gray-400 hover:text-red-500 transition-colors" title="Déconnexion">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        </button>
      </div>
    </header>
  `
})
export class HeaderComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}