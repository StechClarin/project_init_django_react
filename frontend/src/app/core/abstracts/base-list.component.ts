import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms'; // <-- Import nécessaire
import { Apollo, QueryRef } from 'apollo-angular';
import { DocumentNode } from 'graphql';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';

@Component({ template: '' })
export abstract class BaseListComponent<T> implements OnInit {

  // 1. INJECTION (Ce qui manquait pour 'this.fb')
  protected apollo = inject(Apollo);
  protected fb = inject(FormBuilder);

  // --- CONFIGURATION ABSTRAITE ---
  abstract query: DocumentNode;
  abstract responseKey: string;

  // 2. CONTRAT (L'enfant DOIT implémenter ça)
  abstract initFilterForm(): FormGroup;

  // --- ÉTAT ---
  // 3. PROPRIÉTÉ (Ce qui manquait pour 'this.filterForm')
  filterForm!: FormGroup;

  items$!: Observable<T[]>;
  isLoading = signal(true);
  queryRef!: QueryRef<any>;

  ngOnInit(): void {
    // 4. INITIALISATION DU FORMULAIRE
    // On appelle la méthode de l'enfant pour créer le formulaire
    this.filterForm = this.initFilterForm();

    // Par défaut, on lance la requête tout de suite
    // L'enfant peut surcharger ngOnInit sans appeler super.ngOnInit() s'il veut différer
    this.initQuery();
  }

  protected initQuery(): void {
    // On lance la requête Apollo avec les valeurs initiales du formulaire
    this.queryRef = this.apollo.watchQuery({
      query: this.query,
      variables: this.filterForm.value,
      notifyOnNetworkStatusChange: true
    });

    this.items$ = this.queryRef.valueChanges.pipe(
      tap(result => this.isLoading.set(result.loading)),
      map((result: any) => result.data[this.responseKey])
    );
  }

  refresh() {
    // On utilise les valeurs actuelles du formulaire pour recharger
    this.queryRef.refetch(this.filterForm.value);
  }

  onFiltersChanged(filters: any) {
    this.filterForm.patchValue(filters);
    this.refresh();
  }
}
