import React from "react";
import {useGetTransportListQuery} from "./transportConfigSlice";

import {TransportList} from "./TransportList";

function TransportView() {
    const transportList = useGetTransportListQuery().data || [];
    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <h1>Transport View</h1>
            <TransportList transports={transportList}/>
        </div>
    );
}

export default TransportView; 