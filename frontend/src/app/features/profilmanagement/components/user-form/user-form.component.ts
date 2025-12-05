import { Component, inject, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Apollo } from 'apollo-angular';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { UiInputComponent } from '@shared/components/ui-input/ui-input.component';
import { UserService } from '../../services/user.service';
import { GET_ALL_ROLES } from '../../graphql/role.queries';
import { BaseFormComponent } from '@core/abstracts/base-form.component';
import { User } from '../../models/user.model';
import { CustomValidators } from '@core/validators/custom-validators';

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, UiInputComponent],
  template: `
    <div class="bg-white rounded-xl shadow-xl border border-gray-200 max-w-2xl mx-auto">
      
      <div class="p-6 border-b border-gray-100">
        <h2 class="text-xl font-bold text-gray-800">{{ user ? 'Modifier l\\'Utilisateur' : 'Nouvel Utilisateur' }}</h2>
      </div>

      <div class="p-6">
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <app-ui-input
              label="Nom d'utilisateur"
              [control]="form.controls.username"
              [required]="true"
              placeholder="ex: jdupont"
            ></app-ui-input>

            <app-ui-input
              label="Email professionnel"
              type="email"
              [control]="form.controls.email"
              [required]="true"
              placeholder="jean.dupont@company.com"
            ></app-ui-input>

          </div>

          <!-- Sélection du Rôle -->
          <div class="mb-4">
            <label for="role" class="block text-sm font-medium text-gray-700 mb-1">
              Rôle <span class="text-red-500">*</span>
            </label>
            <select
              id="role"
              formControlName="role"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option [ngValue]="null" disabled>Sélectionnez un rôle</option>
              <option *ngFor="let role of roles$ | async" [ngValue]="role.id">
                {{ role.name }}
              </option>
            </select>
            <div *ngIf="form.controls.role.invalid && (form.controls.role.dirty || form.controls.role.touched)" class="text-red-600 text-sm mt-1">
              Le rôle est requis.
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <app-ui-input
                label="Mot de passe"
                type="password"
                [control]="form.controls.password"
                [required]="!user"
              ></app-ui-input>

              <app-ui-input
                label="Confirmation"
                type="password"
                [control]="form.controls.password2"
                [required]="!user"
                errorMessage="Les mots de passe ne correspondent pas."
              ></app-ui-input>
          </div>

          <!-- Message d'erreur global -->
          <div *ngIf="errorMessage" class="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
            {{ errorMessage }}
          </div>

          <div class="flex justify-end mt-6 pt-4 border-t border-gray-100">
            <button 
              type="button" 
              (click)="onCancel()"
              class="mr-3 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
              Annuler
            </button>
            
            <button 
              type="submit" 
              [disabled]="form.invalid || isSubmitting"
              class="px-6 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-md flex items-center">
              <span *ngIf="isSubmitting" class="mr-2">
                <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ user ? 'Modifier' : 'Créer' }} l'utilisateur
            </button>
          </div>
        </form>
      </div>
    </div>
  `
})
export class UserFormComponent extends BaseFormComponent implements OnInit, OnChanges {
  private fb = inject(FormBuilder);
  private userService = inject(UserService);
  private apollo = inject(Apollo);

  @Input() user: User | null = null;

  roles$!: Observable<any[]>;

  // Définition stricte du formulaire (Logique Métier)
  // On utilise 'form' (hérité) au lieu de 'userForm'
  // @ts-ignore: On force le typage pour le moment car BaseFormComponent a FormGroup générique
  override form = this.fb.nonNullable.group({
    username: ['', [Validators.required, Validators.minLength(3)]],
    email: ['', [Validators.required, Validators.email]],
    role: ['', [Validators.required]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    password2: ['', [Validators.required]]
  }, { validators: CustomValidators.match('password', 'password2') });

  ngOnInit() {
    // Chargement des rôles via GraphQL
    this.roles$ = this.apollo
      .watchQuery({ query: GET_ALL_ROLES })
      .valueChanges.pipe(
        map((result: any) => result.data.roles)
      );
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['user']) {
      if (this.user) {
        // Mode Édition
        this.form.patchValue({
          username: this.user.username,
          email: this.user.email,
          role: this.user.roles?.[0]?.id || '' // On prend l'ID du premier rôle ou vide
        });

        // En édition, le mot de passe est optionnel
        this.form.controls.password.clearValidators();
        this.form.controls.password.updateValueAndValidity();
        this.form.controls.password2.clearValidators();
        this.form.controls.password2.updateValueAndValidity();
      } else {
        // Mode Création (Reset)
        this.form.reset();
        this.form.controls.password.setValidators([Validators.required, Validators.minLength(6)]);
        this.form.controls.password.updateValueAndValidity();
        this.form.controls.password2.setValidators([Validators.required]);
        this.form.controls.password2.updateValueAndValidity();
      }
    }
  }

  onSubmit() {
    // Validation spécifique avant soumission (ex: password match)
    // Géré par le CustomValidator désormais

    // On appelle la méthode submit() du parent qui gère le loading, save(), success/error
    super.submit();
  }

  // Implémentation de la méthode abstraite save()
  save(): Observable<any> {
    // Mapping pour le backend : 'role' (front) -> 'roles' (back)
    const payload: any = {
      ...this.form.value,
      roles: [this.form.value.role]
    };

    // Si on est en édition, on ajoute l'ID
    if (this.user && this.user.id) {
      payload.id = this.user.id;
      // Si le mot de passe est vide, on ne l'envoie pas pour ne pas l'écraser
      if (!payload.password) {
        delete payload.password;
        delete payload.password2;
      }
    }

    return this.userService.save(payload);
  }
}