import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Store } from '@ngrx/store';
import { AsyncPipe, JsonPipe } from '@angular/common'; // Utile pour le debug
import { UiActions } from './state/ngrx/ui/ui.actions';
import { selectIsSidebarOpen } from './state/ngrx/ui/ui.reducer';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, AsyncPipe, JsonPipe],
  template: `
    <router-outlet></router-outlet>
  `
})
export class AppComponent {
  private store = inject(Store);

  isSidebarOpen$ = this.store.select(selectIsSidebarOpen);

  toggleSidebar() {
    this.store.dispatch(UiActions.toggleSidebar());
  }
}
