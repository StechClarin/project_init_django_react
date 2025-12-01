import { ApplicationConfig, provideZoneChangeDetection, isDevMode, APP_INITIALIZER } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideStore, provideState } from '@ngrx/store';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { UserFeature } from './features/profilmanagement/store/user/user.store';
import { DynamicRouterService } from './core/routing/dynamic-router.service';
import { routes } from './app.routes';
import { graphqlProvider } from './core/providers/graphql.provider';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { graphqlNameInterceptor } from './core/interceptors/graphql-name.interceptor'; // <-- IMPORT

export function initializeRoutes(dynamicRouter: DynamicRouterService) {
  return () => dynamicRouter.loadDynamicRoutes();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),

    // 1. HTTP Client (Obligatoire pour Apollo)
    provideHttpClient(),
    provideRouter(routes), // Tes routes statiques de base (Login, etc.)
    {
      provide: APP_INITIALIZER,
      useFactory: initializeRoutes,
      deps: [DynamicRouterService],
      multi: true // Important : ne pas écraser les autres inits
    },
    // 2. Apollo (Data Serveur)
    graphqlProvider,
    provideHttpClient(withInterceptors([authInterceptor])), // <--- AJOUTE LE ICI

    provideHttpClient(withInterceptors([
      authInterceptor,      // 1. On met le Token
      graphqlNameInterceptor // 2. On renomme l'URL pour l'affichage
    ])),

    // 3. NgRx (Data Client)
    provideStore(),
    provideState(UserFeature),
    provideStoreDevtools({ maxAge: 25, logOnly: !isDevMode() })
  ]
};