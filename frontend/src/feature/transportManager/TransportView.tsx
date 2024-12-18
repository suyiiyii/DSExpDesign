import React from "react";
import {useDeleteTransportMutation, useGetTransportListQuery} from "./transportConfigSlice";

import {TransportList} from "./TransportList";
import {City, ResultStatus, Transport} from "../../utils/types";
import {enqueueSnackbar, SnackbarProvider} from "notistack";
import {TransportForm} from "./TransportForm";
import {Box, MenuItem, TextField} from "@mui/material";
import {useGetCityListQuery} from "../cityManager/cityConfigSlice";


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

    const initialFilterForm = {
        type: "none",
        start: "none",
        end: "none",
    }
    const cities = useGetCityListQuery().data || [];
    const [filterForm, setFilterForm] = React.useState(initialFilterForm);
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFilterForm({...filterForm, [name]: value});
    };

    function disableOption(option: City) {
        return option.name === filterForm.start || option.name === filterForm.end
    }

    function filteredTransprots(transportList: Transport[]) {
        return transportList.filter(transport => {
            if (filterForm.type !== "none" && transport.type !== filterForm.type) {
                return false;
            }
            if (filterForm.start !== "none" && transport.start !== filterForm.start) {
                return false;
            }
            if (filterForm.end !== "none" && transport.end !== filterForm.end) {
                return false;
            }
            return true;
        });
    }


    const transportList = useGetTransportListQuery().data || [];
    return (
        <>
            <SnackbarProvider/>
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <Box component="form" sx={{display: 'flex', flexDirection: 'row', gap: 2}}>
                    <TextField
                        select
                        label="类型"
                        name="type"
                        value={filterForm.type}
                        onChange={handleChange}
                        required
                    >
                        <MenuItem value="none">None</MenuItem>
                        <MenuItem value="train">Train</MenuItem>
                        <MenuItem value="flight">Flight</MenuItem>
                    </TextField>
                    <TextField
                        select
                        label="起始城市"
                        name="start"
                        value={filterForm.start}
                        onChange={handleChange}
                        required
                    >
                        <MenuItem value="none">None</MenuItem>
                        {cities.filter((city) =>{
                            for (const transport of filteredTransprots(transportList)) {
                                if (city.name === transport.start) {
                                    return true;
                                }
                            }
                            return false;
                        }).map((city) => (
                            <MenuItem key={city.name} value={city.name} disabled={disableOption(city)}>
                                {city.name}
                            </MenuItem>
                        ))}
                    </TextField>
                    <TextField
                        select
                        label="到达城市"
                        name="end"
                        value={filterForm.end}
                        onChange={handleChange}
                        required
                    >
                        <MenuItem value="none">None</MenuItem>
                        {cities.filter((city)=>{
                            for (const transport of filteredTransprots(transportList)) {
                                if (city.name === transport.end) {
                                    return true;
                                }
                            }
                            return false;
                        }).map((city) => (
                            <MenuItem key={city.name} value={city.name} disabled={disableOption(city)}>
                                {city.name}
                            </MenuItem>
                        ))}
                    </TextField>
                </Box>
                <h1>Transport View</h1>
                <TransportList transports={filteredTransprots(transportList)} doDelete={doDeleteTransport}/>
                <h2>Add Transport</h2>
                <TransportForm/>
            </div>
        </>
    );
}

export default TransportView; 