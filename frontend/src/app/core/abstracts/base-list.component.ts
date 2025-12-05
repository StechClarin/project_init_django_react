import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms'; // N'oublie pas ces imports
import { Apollo, QueryRef } from 'apollo-angular';
import { DocumentNode } from 'graphql';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { ToastService } from '@core/services/toast.service';

@Component({ template: '' })
export abstract class BaseListComponent<T> implements OnInit {
  protected apollo = inject(Apollo);
  protected fb = inject(FormBuilder); // Important pour l'enfant

  abstract query: DocumentNode;
  abstract responseKey: string;
  abstract initFilterForm(): FormGroup;

  filterForm!: FormGroup;
  items$!: Observable<T[]>;
  isLoading = signal(true);
  queryRef!: QueryRef<any>;

  // Pagination State
  currentPage = signal(1);
  pageSize = signal(10);
  totalCount = signal(0);
  numPages = signal(0);

  ngOnInit(): void {
    this.filterForm = this.initFilterForm();
    this.initQuery();
  }

  protected initQuery(): void {
    this.queryRef = this.apollo.watchQuery({
      query: this.query,
      variables: {
        ...this.filterForm.value,
        page: this.currentPage(),
        pageSize: this.pageSize()
      },
      notifyOnNetworkStatusChange: true,
      fetchPolicy: 'network-only'
    });

    this.items$ = this.queryRef.valueChanges.pipe(
      tap(result => this.isLoading.set(result.loading)),
      map((result: any) => {
        const data = result.data[this.responseKey];
        // Auto-update pagination metadata if available
        if (data && data.totalCount !== undefined) {
          this.totalCount.set(data.totalCount);
          this.numPages.set(data.numPages);
          // If the response has 'items', return that, otherwise return the data itself
          return data.items || data;
        }
        return data;
      })
    );
  }

  refresh() {
    this.queryRef.refetch({
      ...this.filterForm.value,
      page: this.currentPage(),
      pageSize: this.pageSize()
    });
  }

  // Pagination Methods
  nextPage() {
    if (this.currentPage() < this.numPages()) {
      this.currentPage.update(p => p + 1);
      this.refresh();
    }
  }

  prevPage() {
    if (this.currentPage() > 1) {
      this.currentPage.update(p => p - 1);
      this.refresh();
    }
  }

  goToPage(page: number) {
    if (page >= 1 && page <= this.numPages()) {
      this.currentPage.set(page);
      this.refresh();
    }
  }
  // Service pour les opérations d'écriture (REST)
  abstract service: any; // On utilise any ou une interface commune si possible (ex: BaseService)
  protected toastService = inject(ToastService);

  // Status Toggle Generic
  toggleStatus(item: any) {
    if (!item || !item.id) return;

    // On suppose que l'item a une propriété isActive ou is_active
    // Mais le backend renvoie souvent isActive en camelCase via GraphQL
    // Le service attend l'ID.

    this.service.status(item.id).subscribe({
      next: (updatedItem: any) => {
        // On peut soit rafraîchir toute la liste
        this.refresh();
        // Soit mettre à jour localement si on veut être optimiste (mais refresh est plus sûr)
        const status = updatedItem.isActive ?? updatedItem.is_active;
        this.toastService.success(`Statut modifié avec succès.`);
      },
      error: (err: any) => {
        console.error('Error toggling status:', err);
        this.toastService.error('Une erreur est survenue lors du changement de statut.');
      }
    });
  }
}