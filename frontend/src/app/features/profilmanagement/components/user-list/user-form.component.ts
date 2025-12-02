import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { UiInputComponent } from '@shared/components/ui-input/ui-input.component'; // <-- Import magique

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, UiInputComponent],
  template: `
    <div class="p-6 bg-white rounded-xl shadow-sm border border-gray-200 max-w-2xl mx-auto mt-10">
      
      <h2 class="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Nouvel Utilisateur</h2>

      <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <app-ui-input
            label="Nom d'utilisateur"
            [control]="userForm.controls.username"
            [required]="true"
            placeholder="ex: jdupont"
          ></app-ui-input>

          <app-ui-input
            label="Email professionnel"
            type="email"
            [control]="userForm.controls.email"
            [required]="true"
            placeholder="jean.dupont@company.com"
          ></app-ui-input>

        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <app-ui-input
                label="Mot de passe"
                type="password"
                [control]="userForm.controls.password"
                [required]="true"
            ></app-ui-input>

            <app-ui-input
                label="Confirmation"
                type="password"
                [control]="userForm.controls.password2"
                [required]="true"
            ></app-ui-input>
        </div>

        <div class="flex justify-end mt-6 pt-4 border-t border-gray-100">
          <button 
            type="button" 
            class="mr-3 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
            Annuler
          </button>
          
          <button 
            type="submit" 
            [disabled]="userForm.invalid"
            class="px-6 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-md">
            Créer l'utilisateur
          </button>
        </div>

      </form>
    </div>
  `
})
export class UserFormComponent {
  private fb = inject(FormBuilder);

  // Définition stricte du formulaire (Logique Métier)
  userForm = this.fb.nonNullable.group({
    username: ['', [Validators.required, Validators.minLength(3)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    password2: ['', [Validators.required]]
  });

  onSubmit() {
    if (this.userForm.valid) {
      console.log('Payload prêt à envoyer :', this.userForm.value);
      // Ici on appellera UserService.save(this.userForm.value)
    } else {
      // Petite astuce UX : Si l'user clique sans remplir, on marque tout comme touché pour afficher les erreurs rouges
      this.userForm.markAllAsTouched();
    }
  }
}