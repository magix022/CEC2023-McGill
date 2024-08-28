import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { Algo2Component } from './components/algo2/algo2.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PlotlyModule } from 'angular-plotly.js';
import { Algo1Component } from './components/algo1/algo1.component';
import { Algo4Component } from './components/algo4/algo4.component';
import { Algo3Component } from './components/algo3/algo3.component';


const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'Algo1',
    component: Algo1Component,
  },
  {
    path: 'Algo2',
    component: Algo2Component,
  },
  {
    path: 'Algo3',
    component: Algo3Component,
  },
  {
    path: 'Algo4',
    component: Algo4Component,
  },
];


@NgModule({
  declarations: [
    HomeComponent,
    Algo1Component,
    Algo2Component,
    Algo3Component,
    Algo4Component,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule,
    PlotlyModule,
    FormsModule
  ],
  exports: [
    RouterModule
  ]
})
export class CoreModule { }
