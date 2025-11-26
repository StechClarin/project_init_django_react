import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login.component';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';

export const routes: Routes = [
  // 1. Route Publique (Login)
  // C'est la seule page accessible sans le layout principal
  { 
    path: 'login', 
    component: LoginComponent 
  },

  // 2. Routes Protégées (Dans le Layout Admin)
  // Tout ce qui est ici aura la Sidebar et le Header
  {
    path: '',
    component: MainLayoutComponent,
    // canActivate: [authGuard], // (À décommenter plus tard quand le guard sera prêt)
    children: [
      // Redirection par défaut vers le dashboard
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      
      // Le Dashboard (Lazy loaded)
      { 
        path: 'dashboard', 
        loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent) 
      },
      
      // Module Produits (Lazy loaded)
    //   { 
    //     path: 'products', 
    //     loadChildren: () => import('./features/products/products.routes').then(m => m.PRODUCT_ROUTES) 
    //   },
      
      // Module Utilisateurs/Profil (Lazy loaded)
    //   { 
    //     path: 'users', 
    //     loadChildren: () => import('./features/profilmanagement/profil.routes').then(m => m.PROFIL_ROUTES) 
    //   }
    ]
  },

  // 3. Fallback (404)
  // Si l'URL n'existe pas, on renvoie vers la racine (qui redirige vers dashboard ou login)
  { path: '**', redirectTo: '' }
];