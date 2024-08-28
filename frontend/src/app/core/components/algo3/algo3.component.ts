import { Component } from '@angular/core';
import data from './algo3output.json';

@Component({
  selector: 'app-form',
  templateUrl: './algo3.component.html',
  styleUrls: ['./algo3.component.scss']
})
export class Algo3Component {

  x1: any[] = [];
  y1: any[] = [];
  dropdownData: any[] = [];
  dropdownSelected: any;
  dropdownData2: any[] = [];
  dropdownSelected2: any;


  points1 = {
    x: [] as any[],
    y: [] as any[],
    name: 'scatter',
    type: 'bar',
  };

  graph1 = {
    data: [this.points1],
    layout: {
      title: {
        text:'Algorithm 3: Money Per Country',
        font: {
          family: 'Courier New, monospace',
          size: 26
        },
        xref: 'paper',
        x: 0.05,
      },
      width: 10000,

      xaxis: {
        title: "Country",
        font: {
          family: 'Courier New, monospace',
          size: 26
        },
      },
      yaxis: {},
    },
    config: {
      displaylogo: false,
      showTips: false,
      modeBarButtonsToRemove: []
    }
  };

  points2 = {
    x: [] as any[],
    y: [] as any[],
    name: 'scatter',
    type: 'bar',
  };

  graph2 = {
    data: [this.points2],
    layout: {
      title: {
        text:'Algorithm 3: Resources Per Country By Sector',
        font: {
          family: 'Courier New, monospace',
          size: 26
        },
        xref: 'paper',
        x: 0.05,
      },
    //   width: 100,

      xaxis: {
        title: "Sector",
        font: {
          family: 'Courier New, monospace',
          size: 26
        },
      },
      yaxis: {},
    },
    config: {
      displaylogo: false,
      showTips: false,
      modeBarButtonsToRemove: []
    }
  };

  points3 = {
    x: [] as any[],
    y: [] as any[],
    name: 'scatter',
    type: 'bar',
  };

  graph3 = {
    data: [this.points3],
    layout: {
      title: {
        text:'Algorithm 3: Country By Resource',
        font: {
          family: 'Courier New, monospace',
          size: 26
        },
        xref: 'paper',
        x: 0.05,
      },
    //   width: 100,

      xaxis: {
        title: "Country",
        font: {
          family: 'Courier New, monospace',
          size: 26
        },
      },
      yaxis: {},
    },
    config: {
      displaylogo: false,
      showTips: false,
      modeBarButtonsToRemove: []
    }
  };

  ngOnInit(): void {
    let dataset = data["MoneyPerCountry"]
    for (let [k, v] of Object.entries(dataset)) {
      this.x1.push(k);
      this.y1.push(v);
    }
    this.points1.x = this.x1;
    this.points1.y = this.y1;

    dataset = data["ResourcesPerCountryBySector"]
    console.log(dataset)

    for (let [k, v] of Object.entries(dataset)) {
      this.dropdownData?.push({
        key: k,
        value: JSON.stringify(v)
      })
    }

    dataset = data["CountryPerResource"]

    for (let [k, v] of Object.entries(dataset)) {
      this.dropdownData2?.push({
        key: k,
        value: JSON.stringify(v)
      })
    }
  }

  onOptionsSelected(event: any) {
    const value = JSON.parse(event.target.value);
    this.points2.x = Object.keys(value);
    this.points2.y = Object.values(value);
 }

 onOptionsSelected2(event: any) {
  const value = JSON.parse(event.target.value);
  this.points3.x = Object.keys(value);
  this.points3.y = Object.values(value);
}
  
}
