// src/app/state/ngrx/ui/ui.actions.ts
import { createActionGroup, emptyProps, props } from '@ngrx/store';

export const UiActions = createActionGroup({
  source: 'UI', // Le préfixe pour le débug
  events: {
    'Toggle Sidebar': emptyProps(), // Juste une action simple
    'Set Dark Mode': props<{ isDark: boolean }>(), // Une action avec des données
  },
});