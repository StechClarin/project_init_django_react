import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { User } from '../../models/user.model';
import { UiCardComponent } from '@shared/components/ui-card/ui-card.component';
import { UiAvatarComponent } from '@shared/components/ui-avatar/ui-avatar.component';
import { UiStatusBadgeComponent } from '@shared/components/ui-status-badge/ui-status-badge.component';

@Component({
  selector: 'app-user-detail',
  standalone: true,
  imports: [CommonModule, UiCardComponent, UiAvatarComponent, UiStatusBadgeComponent],
  template: `
    <app-ui-card>
      
      <!-- Header -->
      <div header class="flex items-center space-x-6">
        <app-ui-avatar [name]="user?.username || ''" size="xl"></app-ui-avatar>
        <div>
          <h2 class="text-3xl font-bold">{{ user?.username }}</h2>
          <p class="text-indigo-200 mt-1">{{ user?.email }}</p>
          <div class="mt-3 flex gap-2">
              <span class="px-3 py-1 rounded-full text-xs font-medium bg-white/10 border border-white/20">
                  {{ user?.roles?.[0]?.name || 'Aucun rôle' }}
              </span>
              <app-ui-status-badge [isActive]="user?.isActive || false" activeLabel="Actif" inactiveLabel="Inactif"></app-ui-status-badge>
          </div>
        </div>
      </div>

      <!-- Corps avec détails -->
      <div content class="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          <div class="space-y-4">
              <div>
                  <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Prénom</label>
                  <p class="text-gray-800 font-medium text-lg">{{ user?.firstName || '-' }}</p>
              </div>
              <div>
                  <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Nom</label>
                  <p class="text-gray-800 font-medium text-lg">{{ user?.lastName || '-' }}</p>
              </div>
          </div>

          <div class="space-y-4">
              <div>
                  <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Date d'inscription</label>
                  <p class="text-gray-800 font-medium text-lg">{{ user?.dateJoined | date:'mediumDate' }}</p>
              </div>
              <div>
                  <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">ID Utilisateur</label>
                  <p class="text-gray-500 text-sm font-mono truncate" title="{{ user?.id }}">{{ user?.id }}</p>
              </div>
          </div>

      </div>

      <!-- Footer -->
      <div footer>
        <button 
          (click)="onClose()"
          class="px-6 py-2 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 hover:text-gray-900 transition shadow-sm">
          Fermer
        </button>
      </div>

    </app-ui-card>
  `
})
export class UserDetailComponent {
  @Input() user: User | null = null;
  @Output() close = new EventEmitter<void>();

  onClose() {
    this.close.emit();
  }
}
