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
    // 1. Le parent initialise 'this.filterForm' via 'initFilterForm'
    super.ngOnInit();

    // 2. Maintenant 'this.filterForm' existe, on peut le patcher
    this.store.select(selectUserFilters).pipe(take(1)).subscribe(filters => {
      if (filters && Object.keys(filters).length > 0) {
        this.filterForm.patchValue(filters);
        this.refresh();
      }
    });
  }

  override refresh() {
    this.store.dispatch(UserActions.setFilters({ filters: this.filterForm.value }));
    super.refresh();
  }
}