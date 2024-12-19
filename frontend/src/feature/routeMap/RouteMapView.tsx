import React, {Fragment, useEffect, useState} from "react";
import MermaidChart from "../../utils/mermaid/MermaidChart";
import {useGetRouteMapQuery} from "./routeMapSlice";

async function sha1(message: string): Promise<string> {
    // Encode the message as an ArrayBuffer
    const msgBuffer = new TextEncoder().encode(message);

    // Calculate the SHA-1 hash
    const hashBuffer = await crypto.subtle.digest('SHA-1', msgBuffer);

    // Convert the ArrayBuffer to a hexadecimal string
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

    return hashHex;
}

export default function RouteMapView() {
    const {data: chartData} = useGetRouteMapQuery();
    const [chart, setChart] = useState({data: "", id: ""});

    useEffect(() => {
        if (chartData) {
            sha1(chartData.data).then(hash => {
                setChart({data: chartData.data, id: hash});
            });
        }
    }, [chartData]);
    // 使用 data 的哈希作为 key，避免相同位置重复渲染导致的 mermaid 无法正常显示的问题

    return (
        <div>
            <h1>Route Map</h1>
            {chart.data === "" ? (
                <div>loading...</div>
            ) : (
                <Fragment key={chart.id}>
                    <MermaidChart chart={chart.data}/>
                </Fragment>
            )}
        </div>
    );
}