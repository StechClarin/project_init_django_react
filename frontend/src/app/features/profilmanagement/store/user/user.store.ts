import { createFilterStore } from '../../../../core/store/filter.factory';

export interface UserFilters {
    username?: string;
    role?: string;
}

const initialFilters: UserFilters = {};

export const {
    actions: UserActions,
    feature: UserFeature,
    selectors: selectUserFilters
} = createFilterStore<UserFilters>('user', 'User List', initialFilters);
