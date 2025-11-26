// src/app/state/ngrx/ui/ui.reducer.ts
import { createFeature, createReducer, on } from '@ngrx/store';
import { UiActions } from './ui.actions';

// 1. L'interface de notre état
export interface UiState {
  isSidebarOpen: boolean;
  isDarkMode: boolean;
}

// 2. L'état initial
const initialState: UiState = {
  isSidebarOpen: true, // Ouverte par défaut
  isDarkMode: false,
};

// 3. La Feature (Reducer + Selectors automatiques !)
export const uiFeature = createFeature({
  name: 'ui', // Le nom dans le store JSON global
  reducer: createReducer(
    initialState,
    
    // Quand on reçoit l'ordre "Toggle Sidebar", on inverse la valeur
    on(UiActions.toggleSidebar, (state) => ({
      ...state,
      isSidebarOpen: !state.isSidebarOpen,
    })),

    // Quand on reçoit l'ordre "Set Dark Mode"
    on(UiActions.setDarkMode, (state, action) => ({
      ...state,
      isDarkMode: action.isDark,
    }))
  ),
});

// On exporte les propriétés pour faciliter l'accès (Optionnel mais pratique)
export const {
  name,
  reducer,
  selectIsSidebarOpen,
  selectIsDarkMode,
  selectUiState,
} = uiFeature;