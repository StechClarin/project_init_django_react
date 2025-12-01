import { Injectable, inject } from '@angular/core';
import { Router, Routes, Route } from '@angular/router';
import { Apollo } from 'apollo-angular';
import { gql } from 'apollo-angular';
import { map, tap } from 'rxjs/operators';
import { firstValueFrom } from 'rxjs';
import { COMPONENT_REGISTRY } from './component.registry';

// La Query pour récupérer juste les liens
const GET_ALL_PAGES = gql`
  query modules {
    
    modules {
      name
      pages {
        title
        icon
        link
      }
    }
  }
`;

@Injectable({ providedIn: 'root' })
export class DynamicRouterService {
  private apollo = inject(Apollo);
  private router = inject(Router);

  async loadDynamicRoutes(): Promise<void> {
    console.log('🔄 Chargement des routes dynamiques...');

    try {
      // 1. On récupère la structure depuis Django
      console.log('Fetching modules from GraphQL...');
      const result: any = await firstValueFrom(
        this.apollo.query({ query: GET_ALL_PAGES })
      );
      console.log('Modules fetched:', result);

      const modules = result.data.modules;
      const dynamicRoutes: Routes = [];

      // 2. On parcourt chaque module et chaque page
      modules.forEach((mod: any) => {
        mod.pages.forEach((page: any) => {
          const link = page.link; // ex: "/users"

          // 3. On vérifie si on a le composant dans notre registre
          if (COMPONENT_REGISTRY[link]) {

            // On crée la route Angular
            // On retire le "/" au début (Angular préfère "users" à "/users")
            const path = link.startsWith('/') ? link.substring(1) : link;

            dynamicRoutes.push({
              path: path,
              loadComponent: COMPONENT_REGISTRY[link] // Lazy loading magique
            });

          } else {
            console.warn(`⚠️ Page en BDD "${link}" sans composant Angular correspondant dans le registre.`);
          }
        });
      });

      // 4. On injecte ces routes dans le MainLayout
      // On récupère la config actuelle
      const currentConfig = this.router.config;

      // On trouve la route qui a le MainLayout (celle qui a path: '')
      const layoutRoute = currentConfig.find(r => r.path === '' && r.children);

      if (layoutRoute && layoutRoute.children) {
        // On ajoute nos routes dynamiques aux enfants du Layout
        layoutRoute.children.push(...dynamicRoutes);

        // On applique la nouvelle config
        this.router.resetConfig(currentConfig);
        console.log('✅ Routes dynamiques chargées :', dynamicRoutes.map(r => r.path));
      }

    } catch (error) {
      console.error('❌ Erreur chargement routes dynamiques', error);
      // On ne bloque pas l'app, on continue avec les routes statiques
    }
  }
}