import React from "react";
import {useDeleteTransportMutation, useGetTransportListQuery} from "./transportConfigSlice";

import {TransportList} from "./TransportList";
import {ResultStatus, Transport} from "../../utils/types";
import {enqueueSnackbar, SnackbarProvider} from "notistack";
import {TransportForm} from "./TransportForm";


function TransportView() {
    const [deleteTransport] = useDeleteTransportMutation();

    function doDeleteTransport(transport: Transport) {
        deleteTransport(transport).unwrap().then((payload) => {
            const value = payload as unknown as ResultStatus;
            if (value.status === "error") {
                enqueueSnackbar("删除失败 " + value.msg, {variant: "error"});
                return;
            }
            enqueueSnackbar("删除成功 " + value.msg, {variant: "success"});
        })
    }


    const transportList = useGetTransportListQuery().data || [];
    return (
        <>
            <SnackbarProvider/>
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <h1>Transport View</h1>
                <TransportList transports={transportList} doDelete={doDeleteTransport} isVirtual={true}/>
                <h2>Add Transport</h2>
                <TransportForm/>
            </div>
        </>
    );
}

export default TransportView; 