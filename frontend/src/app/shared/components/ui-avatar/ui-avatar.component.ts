import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-ui-avatar',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div [class]="containerClasses">
      <div [class]="avatarClasses">
        {{ initials }}
      </div>
    </div>
  `
})
export class UiAvatarComponent {
    @Input() name: string = '';
    @Input() size: 'sm' | 'md' | 'lg' | 'xl' = 'md';

    get initials(): string {
        return this.name ? this.name.charAt(0).toUpperCase() : '?';
    }

    get containerClasses(): string {
        switch (this.size) {
            case 'sm': return 'h-8 w-8 flex-shrink-0';
            case 'lg': return 'h-16 w-16 flex-shrink-0';
            case 'xl': return 'h-20 w-20 flex-shrink-0';
            case 'md': default: return 'h-11 w-11 flex-shrink-0';
        }
    }

    get avatarClasses(): string {
        const base = 'rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold shadow-sm ring-2 ring-white';
        switch (this.size) {
            case 'sm': return `${base} h-8 w-8 text-xs`;
            case 'lg': return `${base} h-16 w-16 text-xl`;
            case 'xl': return `${base} h-20 w-20 text-2xl border-4 border-white/20`;
            case 'md': default: return `${base} h-11 w-11 text-lg group-hover:scale-105 transition-transform duration-200`;
        }
    }
}
