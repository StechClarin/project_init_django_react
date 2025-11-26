import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <aside class="w-64 h-screen bg-slate-900 text-white flex flex-col fixed left-0 top-0 bottom-0 z-50 transition-all duration-300 shadow-xl">
      
      <div class="h-16 flex items-center justify-center border-b border-slate-700">
        <span class="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
          GigaAdmin
        </span>
      </div>

      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        
        <a routerLink="/dashboard" 
           routerLinkActive="bg-indigo-600 text-white shadow-lg shadow-indigo-500/30" 
           class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors group">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          <span class="font-medium">Dashboard</span>
        </a>

        <a routerLink="/users" 
           routerLinkActive="bg-indigo-600 text-white shadow-lg shadow-indigo-500/30"
           class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors group">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <span class="font-medium">Utilisateurs</span>
        </a>

        <a routerLink="/products" 
           routerLinkActive="bg-indigo-600 text-white shadow-lg shadow-indigo-500/30"
           class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors group">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
          <span class="font-medium">Produits</span>
        </a>

      </nav>

      <div class="p-4 border-t border-slate-700">
        <p class="text-xs text-slate-500 text-center">v1.0.0 - GigaCore</p>
      </div>
    </aside>
  `
})
export class SidebarComponent {}