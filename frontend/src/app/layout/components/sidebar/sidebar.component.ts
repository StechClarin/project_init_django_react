import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Apollo } from 'apollo-angular';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { GET_SIDEBAR_MODULES } from './sidebar.queries';

// Interface locale pour typer les données
interface SidebarPage {
  title: string;
  link: string;
  icon: string;
}

interface SidebarModule {
  name: string;
  pages: SidebarPage[];
}

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

      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-6">
        
        <div *ngFor="let module of modules$ | async">
          
          <div class="px-3 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
            {{ module.name }}
          </div>

          <div class="space-y-1">
            <a *ngFor="let page of module.pages"
               [routerLink]="page.link" 
               routerLinkActive="bg-indigo-600 text-white shadow-lg shadow-indigo-500/30"
               class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors group cursor-pointer">
              
              <span class="mr-3">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
              </span>

              <span class="font-medium">{{ page.title }}</span>
            </a>
          </div>

        </div>

        <div *ngIf="!(modules$ | async)" class="text-center text-slate-500 text-sm mt-10">
          Chargement du menu...
        </div>

      </nav>

      <div class="p-4 border-t border-slate-700">
        <p class="text-xs text-slate-500 text-center">v1.0.0 - GigaCore</p>
      </div>
    </aside>
  `
})
export class SidebarComponent implements OnInit {
  private apollo = inject(Apollo);
  
  // Observable qui contient la liste des modules
  modules$!: Observable<SidebarModule[]>;

  ngOnInit() {
    // On récupère les données via GraphQL
    this.modules$ = this.apollo.watchQuery<any>({
      query: GET_SIDEBAR_MODULES
    }).valueChanges.pipe(
      map(result => result.data.modules)
    );
  }
}