import { createActionGroup, createFeature, createReducer, emptyProps, on, props } from '@ngrx/store';

// 1. Définition de l'état générique
export interface FilterState<T> {
    filters: T;
}

/**
 * USINE À STORE DE FILTRES
 * Génère automatiquement Actions + Reducer + Selectors pour une entité.
 * * @param featureKey Le nom unique dans le store (ex: 'userContext')
 * @param source Le nom pour les logs DevTools (ex: 'User List')
 * @param initialFilters Les valeurs par défaut des filtres
 */
export function createFilterStore<T>(
    featureKey: string,
    source: string,
    initialFilters: T
) {

    // A. Génération des Actions Uniques (préfixées par 'source')
    const actions = createActionGroup({
        source: source as any,
        events: {
            'Set Filters': props<{ filters: Partial<T> }>(),
            'Clear Filters': emptyProps(),
        },
    });

    // B. État Initial
    const initialState: FilterState<T> = {
        filters: initialFilters
    };

    // C. Génération du Reducer
    const feature = createFeature({
        name: featureKey,
        reducer: createReducer(
            initialState,

            // Logique de mise à jour (Fusion des filtres existants + nouveaux)
            on(actions.setFilters, (state, { filters }) => ({
                ...state,
                filters: { ...state.filters, ...filters }
            })),

            // Logique de reset
            on(actions.clearFilters, () => initialState)
        ),
    });

    // D. On retourne le tout packagé
    return {
        actions,      // Les commandes (UserActions)
        feature,      // Le reducer (userFeature)
        selectors: feature.selectFilters // Le sélecteur direct (selectFilters)
    };
}