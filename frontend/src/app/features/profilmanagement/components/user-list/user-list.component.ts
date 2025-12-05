import { Component, OnInit, inject, signal, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormBuilder, FormControl } from '@angular/forms';
import { Store } from '@ngrx/store';
import { Observable, Subject } from 'rxjs';
import { map, take, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';

import { BaseListComponent } from '@core/abstracts/base-list.component';
import { User } from '../../models/user.model';
import { GET_ALL_USERS, GET_ALL_ROLES } from '../../graphql/user.queries';
import { UserActions, selectUserFilters } from '../../store/user/user.store';
import { UserFormComponent } from '../user-form/user-form.component';
import { UserDetailComponent } from '../user-detail/user-detail.component';
import { UserService } from '../../services/user.service';
import { UiModalComponent } from '@shared/components/ui-modal/ui-modal.component';
import { ToastService } from '@core/services/toast.service';
import { UiPaginationComponent } from '@shared/components/ui-pagination/ui-pagination.component';

import { UiDropdownComponent } from '@shared/components/ui-dropdown/ui-dropdown.component';
import { UiStatusBadgeComponent } from '@shared/components/ui-status-badge/ui-status-badge.component';
import { UiAvatarComponent } from '@shared/components/ui-avatar/ui-avatar.component';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, UserFormComponent, UiModalComponent, UiPaginationComponent, UiDropdownComponent, UiStatusBadgeComponent, UiAvatarComponent, UserDetailComponent],
  templateUrl: './user-list.component.html'
})
export class UserListComponent extends BaseListComponent<User> implements OnInit, OnDestroy {
  // ... existing code ...

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  query = GET_ALL_USERS;
  responseKey = 'users';

  private store = inject(Store);

  // Utilisateur sélectionné pour édition
  selectedUser = signal<User | null>(null);

  // État de la modale
  isModalOpen = signal(false);
  modalMode = signal<'create' | 'edit' | 'detail' | 'delete'>('create');

  // État du menu d'actions (ID de l'utilisateur dont le menu est ouvert)
  activeMenuId = signal<string | null>(null);

  // Contrôles de formulaire pour les filtres
  protected Math = Math;
  searchControl = new FormControl('');
  isFiltersOpen = signal(false);

  private destroy$ = new Subject<void>();

  openModal(user: User | null = null, mode: 'create' | 'edit' | 'detail' | 'delete' = 'create') {
    this.selectedUser.set(user);
    this.modalMode.set(mode);
    this.isModalOpen.set(true);
  }

  closeModal() {
    this.isModalOpen.set(false);
    this.selectedUser.set(null);
  }

  // Gestion du menu d'actions
  toggleMenu(userId: string, event?: Event) {
    if (event) {
      event.stopPropagation();
    }
    if (this.activeMenuId() === userId) {
      this.closeMenu();
    } else {
      this.activeMenuId.set(userId);
    }
  }

  closeMenu() {
    this.activeMenuId.set(null);
  }

  // Actions
  onEdit(user: User) {
    this.closeMenu();
    this.openModal(user, 'edit');
  }

  public service = inject(UserService); // Public pour être accessible par le template si besoin
  // private toastService = inject(ToastService); // Déjà dans BaseListComponent

  onSeeMore(user: User) {
    console.log('See more user:', user);
    this.closeMenu();
    this.openModal(user, 'detail');
  }

  onDelete(user: User) {
    this.closeMenu();
    this.openModal(user, 'delete');
  }

  confirmDelete() {
    const user = this.selectedUser();
    if (!user) return;

    this.service.delete(user.id).subscribe({
      next: () => {
        this.refresh();
        this.closeModal();
        this.toastService.success(`Utilisateur ${user.username} supprimé avec succès.`);
      },
      error: (err) => {
        console.error('Erreur lors de la suppression', err);
        this.toastService.error('Une erreur est survenue lors de la suppression.');
      }
    });
  }

  onUserCreated() {
    this.closeModal();
    this.refresh(); // On recharge la liste pour voir le nouvel utilisateur
    this.toastService.success('Utilisateur enregistré avec succès.');
  }

  roles$!: Observable<any[]>;

  initFilterForm(): FormGroup {
    return this.fb.group({
      username: [''], // Mappé au searchControl via sync
      email: [''],
      role: ['']
    });
  }

  // Pagination state and methods are now inherited from BaseListComponent

  override ngOnInit(): void {
    // 0. Initialiser le formulaire AVANT tout le reste
    this.filterForm = this.initFilterForm();

    // Charger les rôles pour le filtre
    this.roles$ = this.apollo.watchQuery<any>({
      query: GET_ALL_ROLES
    }).valueChanges.pipe(
      map(result => result.data.roles)
    );

    // 1. Initialisation de la requête (QueryRef) via le parent
    this.initQuery();

    // 2. Abonnement aux changements (items$) - Surcharge pour le mapping spécifique si besoin
    // Mais BaseListComponent le fait déjà bien. Si on veut juste le mapping standard:
    // On peut laisser initQuery faire son travail.
    // Cependant, UserListComponent avait un mapping spécifique pour isLoading.set(false)
    // BaseListComponent le fait aussi maintenant.

    // 3. Restauration des filtres depuis le Store
    this.store.select(selectUserFilters).pipe(take(1)).subscribe(filters => {
      if (filters && Object.keys(filters).length > 0) {
        console.log("⚡ Filtres restaurés, rechargement...", filters);
        this.filterForm.patchValue(filters, { emitEvent: false });
        this.refresh();
      }
    });

    // 4. Synchro Search Input -> Store
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(value => {
      this.filterForm.patchValue({ username: value }, { emitEvent: false });
      this.dispatchFilters();
    });

    // 5. Synchro Filtres Avancés -> Store
    this.filterForm.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.dispatchFilters();
    });
  }

  dispatchFilters() {
    const filters = this.filterForm.value;
    this.store.dispatch(UserActions.setFilters({ filters }));
    this.currentPage.set(1); // Reset page on filter change
    this.refresh();
  }

  toggleFilters() {
    this.isFiltersOpen.update(v => !v);
  }

  resetFilters() {
    this.searchControl.setValue('');
    this.filterForm.reset();
  }

  override refresh() {
    this.store.dispatch(UserActions.setFilters({ filters: this.filterForm.value }));
    super.refresh();
  }
}