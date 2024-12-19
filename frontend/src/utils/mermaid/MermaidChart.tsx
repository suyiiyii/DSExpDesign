import React, {useEffect, useRef} from "react";
import mermaid from "mermaid";

const MermaidChart = ({ chart }:{chart:string}) => {
    const chartRef = useRef(null);

    useEffect(() => {
        mermaid.initialize({ startOnLoad: true });
        mermaid.contentLoaded();
    }, [chart]);

    return (
        <div key={chart}>
            <div className="mermaid" ref={chartRef}>
                {chart}
            </div>
        </div>
    );
};

export default MermaidChart;