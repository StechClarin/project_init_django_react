import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup } from '@angular/forms';
import { Store } from '@ngrx/store';
import { take } from 'rxjs/operators';

import { BaseListComponent } from '@core/abstracts/base-list.component';
import { User } from '../../models/user.model';
import { GET_ALL_USERS } from '../../graphql/user.queries';
import { UserActions, selectUserFilters } from '../../store/user/user.store';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './user-list.component.html',
})
export class UserListComponent extends BaseListComponent<User> implements OnInit {

  query = GET_ALL_USERS;
  responseKey = 'users';

  private store = inject(Store);

  // ✅ Implémentation correcte du contrat
  initFilterForm(): FormGroup {
    // 'this.fb' est maintenant disponible car hérité du parent corrigé
    return this.fb.group({
      search: [''],
      role: [null]
    });
  }

  override ngOnInit(): void {
    // 1. On initialise le formulaire manuellement (sans lancer la requête tout de suite)
    this.filterForm = this.initFilterForm();

    // 2. On récupère les filtres du store
    this.store.select(selectUserFilters).pipe(take(1)).subscribe(filters => {
      if (filters && Object.keys(filters).length > 0) {
        this.filterForm.patchValue(filters);
      }
      // 3. On lance la requête UNE SEULE FOIS avec les bonnes valeurs
      this.initQuery();
    });
  }

  override refresh() {
    this.store.dispatch(UserActions.setFilters({ filters: this.filterForm.value }));
    super.refresh();
  }
}