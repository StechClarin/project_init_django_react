import { Type } from '@angular/core';
import { LoadChildrenCallback } from '@angular/router';

// On définit ici le lien entre l'URL de la BDD et le fichier Angular
// On utilise des fonctions d'import (Lazy Loading) pour la performance
export const COMPONENT_REGISTRY: Record<string, () => Promise<any>> = {
  
  // Clé (URL BDD)      // Valeur (Import du Composant Standalone)
  '/users':             () => import('../../features/profilmanagement/components/user-list/user-list.component').then(m => m.UserListComponent),
  '/roles':             () => import('../../features/profilmanagement/components/role-list/role-list.component').then(m => m.RoleListComponent),
  '/products':          () => import('../../features/products/components/product-list/product-list.component').then(m => m.ProductListComponent),
  
  // Ajoute tes futurs modules ici...
};