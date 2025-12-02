import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { Apollo } from 'apollo-angular';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { GET_SIDEBAR_MODULES } from './sidebar.queries';

// Interface locale
interface SidebarPage {
  id: string;
  title: string;
  link: string;
  icon: string;
}

interface SidebarModule {
  id: string;
  name: string;
  icon: string;
  pages: SidebarPage[];
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <aside class="w-64 h-screen bg-slate-900 flex flex-col fixed left-0 top-0 z-50 shadow-2xl font-sans border-r border-slate-800">
      
      <div class="h-16 flex items-center px-6 border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm">
        <div class="h-8 w-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mr-3 shadow-lg shadow-indigo-500/20">
          <span class="text-white font-bold text-lg">G</span>
        </div>
        <span class="text-xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent tracking-tight">
          GigaCore
        </span>
      </div>

      <nav class="flex-1 overflow-y-auto py-6 px-3 space-y-2 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
        
        <div *ngIf="loading" class="flex flex-col items-center justify-center py-10 space-y-3">
          <div class="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-slate-500 text-xs">Chargement du menu...</span>
        </div>

        <div *ngFor="let module of modules$ | async" class="mb-1">
          
          <button 
            (click)="toggleModule(module.id)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all duration-200 group focus:outline-none">
            
            <div class="flex items-center">
              <span class="mr-3 opacity-70 group-hover:opacity-100 transition-opacity">
                 <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
              </span>
              <span class="text-sm font-semibold tracking-wide uppercase">{{ module.name }}</span>
            </div>

            <svg 
              [class.rotate-180]="isExpanded(module.id)"
              class="w-4 h-4 transition-transform duration-200 opacity-50 group-hover:opacity-100" 
              fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>

          <div 
            *ngIf="isExpanded(module.id)"
            class="mt-1 space-y-1 pl-2 overflow-hidden transition-all duration-300 ease-in-out">
            
            <a *ngFor="let page of module.pages"
               [routerLink]="page.link" 
               routerLinkActive="bg-indigo-600/10 text-indigo-400 border-r-2 border-indigo-500"
               [routerLinkActiveOptions]="{exact: false}"
               class="flex items-center px-4 py-2 text-sm text-slate-400 rounded-md hover:bg-slate-800 hover:text-white transition-colors relative group/page">
              
              <span class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-0 bg-indigo-500 rounded-r transition-all duration-200 group-hover/page:h-4 group-hover/page:opacity-100 opacity-0"></span>

              <span class="mr-3 min-w-[20px] flex justify-center">
                 <svg class="w-1.5 h-1.5 rounded-full bg-current opacity-60 group-hover/page:scale-150 transition-transform" fill="currentColor" viewBox="0 0 8 8"><circle cx="4" cy="4" r="3"/></svg>
              </span>

              <span class="font-medium">{{ page.title }}</span>
            </a>
          </div>

        </div>
      </nav>

      <div class="p-4 border-t border-slate-800 bg-slate-900/50">
        <div class="flex items-center gap-3">
          <div class="h-8 w-8 rounded-full bg-slate-700 flex items-center justify-center text-xs text-white font-bold">
            EN
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">EtherNanos</p>
            <p class="text-xs text-slate-500 truncate">Super Admin</p>
          </div>
        </div>
      </div>
    </aside>
  `
})
export class SidebarComponent implements OnInit {
  private apollo = inject(Apollo);
  private router = inject(Router);
  
  modules$!: Observable<SidebarModule[]>;
  loading = true;

  // État local pour savoir quels modules sont ouverts
  // Clé = ID du module, Valeur = true/false
  expandedModules: Record<string, boolean> = {};

  ngOnInit() {
    this.modules$ = this.apollo.watchQuery<any>({
      query: GET_SIDEBAR_MODULES
    }).valueChanges.pipe(
      tap(() => this.loading = false),
      map(result => {
        const modules = result.data.modules;
        // Optionnel : Ouvrir automatiquement le premier module par défaut
        if (modules.length > 0 && Object.keys(this.expandedModules).length === 0) {
           // this.expandedModules[modules[0].id] = true; 
        }
        return modules;
      })
    );
  }

  // Bascule l'état ouvert/fermé d'un module
  toggleModule(moduleId: string) {
    this.expandedModules[moduleId] = !this.expandedModules[moduleId];
  }

  // Vérifie si un module est ouvert
  isExpanded(moduleId: string): boolean {
    return !!this.expandedModules[moduleId];
  }
}