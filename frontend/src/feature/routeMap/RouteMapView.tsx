import React from "react";
import MermaidChart from "../mermaid/MermaidChart";
  const chartDefinition = `
    graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
  `;

export default function RouteMapView(){

    return (
        <div>
            <h1>Route Map</h1>
            <MermaidChart chart={chartDefinition}></MermaidChart>
        </div>
    )
}