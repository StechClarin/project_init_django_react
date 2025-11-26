import { ApplicationConfig, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

// Imports NgRx
import { provideStore } from '@ngrx/store';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { uiFeature } from './state/ngrx/ui/ui.reducer'; // <-- Importe ta Feature

// Imports Apollo
import { graphqlProvider } from './graphql.provider';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    graphqlProvider,

    // 1. Activer le Store avec notre Feature UI
    provideStore({
      [uiFeature.name]: uiFeature.reducer, 
    }),

    

    provideStoreDevtools({
      maxAge: 25, // Garde les 25 dernières actions en mémoire
      logOnly: !isDevMode(),
      autoPause: true, 
      trace: false, 
      traceLimit: 75, 
    }),

  ]
};

