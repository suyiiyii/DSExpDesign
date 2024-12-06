import React from "react";
import MermaidChart from "../../utils/mermaid/MermaidChart";
import {useGetRouteMapQuery} from "./routeMapSlice";

export default function RouteMapView() {
    const chart = useGetRouteMapQuery().data || {data: ""};
    console.log(chart)
    return (
        <div>
            <h1>Route Map</h1>
            {chart.data === "" ? (
                <div>loading...</div>
            ) : (
                <MermaidChart chart={`${chart.data}`}></MermaidChart>
            )}
        </div>
    )
}