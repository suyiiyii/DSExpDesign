import React, {useState} from "react";
import {Box, Button, MenuItem, TextField} from "@mui/material";
import {City, Transport} from "../../utils/types";
import {useAddTransportMutation} from "./transportConfigSlice";
import {useGetCityListQuery} from "../cityManager/cityConfigSlice";

const initialTransport: Transport = {
    type: "train",
    name: "",
    start: "",
    end: "",
    price: 0,
    start_time: "",
    end_time: "",
    run_id: ""
};

export function TransportForm() {
    const [transport, setTransport] = useState<Transport>(initialTransport);
    const [addTransport] = useAddTransportMutation();
    const cities = useGetCityListQuery().data || [];

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setTransport({...transport, [name]: value});
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        transport.run_id = transport.name
        addTransport(transport);
        setTransport(initialTransport); // Reset form after submission
    };

    function disableOption(option: City) {
        return option.name === transport.start || option.name === transport.end
    }

    function errorCheck() {
        return transport.price <= 0
    }
    return (
        <Box component="form" onSubmit={handleSubmit} sx={{display: 'flex', flexDirection: 'column', gap: 2}}>
            <TextField
                select
                label="类型"
                name="type"
                value={transport.type}
                onChange={handleChange}
                required
            >
                <MenuItem value="train">Train</MenuItem>
                <MenuItem value="flight">Flight</MenuItem>
            </TextField>
            <TextField
                label="名称"
                name="name"
                value={transport.name}
                onChange={handleChange}
                required
            />
            <TextField
                select
                label="起始城市"
                name="start"
                value={transport.start}
                onChange={handleChange}
                required
            >
                {cities.map((city) => (
                    <MenuItem key={city.name} value={city.name} disabled={disableOption(city)}>
                        {city.name}
                    </MenuItem>
                ))}
            </TextField>
            <TextField
                select
                label="到达城市"
                name="end"
                value={transport.end}
                onChange={handleChange}
                required
            >
                {cities.map((city) => (
                    <MenuItem key={city.name} value={city.name} disabled={disableOption(city)}>
                        {city.name}
                    </MenuItem>
                ))}
            </TextField>
            <TextField
                label="价格"
                name="price"
                type="number"
                value={transport.price}
                error={errorCheck()}
                helperText={errorCheck() ? "价格必须大于0" : ""}
                onChange={handleChange}
                required
            />
            <TextField
                label="开始时间"
                name="start_time"
                type="time"
                value={transport.start_time}
                onChange={handleChange}
                required
            />
            <TextField
                label="到站时间"
                name="end_time"
                type="time"
                value={transport.end_time}
                onChange={handleChange}
                required
            />
            {/*<TextField*/}
            {/*    label="Run ID"*/}
            {/*    name="run_id"*/}
            {/*    value={transport.run_id}*/}
            {/*    onChange={handleChange}*/}
            {/*    required*/}
            {/*/>*/}
            <Button type="submit" variant="contained" color="primary" disabled={errorCheck()}>
                Submit
            </Button>
        </Box>
    );
}