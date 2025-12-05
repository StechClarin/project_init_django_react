import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-ui-dropdown',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="relative inline-block text-left">
      <!-- Trigger -->
      <div (click)="onToggle($event)">
        <ng-content select="[trigger]"></ng-content>
      </div>

      <!-- Backdrop transparent pour fermer au clic en dehors -->
      <div *ngIf="isOpen" 
           class="fixed inset-0 z-40 cursor-default" 
           (click)="onClose($event)">
      </div>

      <!-- Menu -->
      <div *ngIf="isOpen" 
           class="absolute right-0 z-50 mt-2 w-48 origin-top-right rounded-xl bg-white shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none animate-in fade-in zoom-in-95 duration-100">
        <div class="py-1" role="none">
            <ng-content select="[menu]"></ng-content>
        </div>
      </div>
    </div>
  `
})
export class UiDropdownComponent {
    @Input() isOpen = false;
    @Output() isOpenChange = new EventEmitter<boolean>();

    onToggle(event: Event) {
        event.stopPropagation();
        this.isOpen = !this.isOpen;
        this.isOpenChange.emit(this.isOpen);
    }

    onClose(event: Event) {
        event.stopPropagation();
        this.isOpen = false;
        this.isOpenChange.emit(false);
    }
}
