import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-ui-input',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule], // Nécessaire pour formControl
  template: `
    <div class="mb-4">
      <label [for]="name" class="block text-sm font-medium text-gray-700 mb-1">
        {{ label }} 
        <span *ngIf="required" class="text-red-500">*</span>
      </label>
      
      <input
        [id]="name"
        [type]="type"
        [formControl]="control"
        [placeholder]="placeholder"
        class="w-full px-4 py-2 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 outline-none"
        [class.border-gray-300]="!hasError()"
        [class.border-red-500]="hasError()"
        [class.bg-red-50]="hasError()"
      />

      <div *ngIf="hasError()" class="mt-1 text-xs text-red-600 flex items-center animate-pulse">
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        
        <span *ngIf="control.errors?.['required']">Ce champ est obligatoire.</span>
        <span *ngIf="control.errors?.['email']">Format d'email invalide.</span>
        <span *ngIf="control.errors?.['minlength']">
          Trop court (min {{ control.errors?.['minlength'].requiredLength }} caractères).
        </span>
        <span *ngIf="control.errors?.['pattern']">Format invalide.</span>
      </div>
    </div>
  `
})
export class UiInputComponent {
  // On force le passage du control et du label (required: true)
  @Input({ required: true }) control!: FormControl;
  @Input({ required: true }) label!: string;
  
  // Optionnels
  @Input() name = 'input-' + Math.random().toString(36).substring(2); // ID unique par défaut
  @Input() type = 'text';
  @Input() placeholder = '';
  @Input() required = false;

  // Helper pour savoir si on affiche l'erreur (seulement si touché ou sale)
  hasError(): boolean {
    return !!(this.control.invalid && (this.control.dirty || this.control.touched));
  }
}