import {Button, FormControl, FormControlLabel, FormLabel, MenuItem, Radio, RadioGroup, TextField} from "@mui/material";
import React, {useEffect, useState} from "react";
import {useGetCityListQuery} from "../cityManager/cityConfigSlice";
import {City} from "../../utils/types";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {planRoute} from "./routePlanSlice";


import {TransportList} from "../transportManager/TransportList";

function time2int(timestr: string): number {
    /** Convert time string to integer */
    const [h, m] = timestr.split(':').map(Number);
    return h * 60 + m;
}

function int2time(minutes: number): string {
    /** Convert integer to time string */
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
}
export default function PlanView() {
    const cityList = useGetCityListQuery().data || []
    const [startCity, setStartCity] = useState("");
    const [endCity, setEndCity] = useState("");
    const [strategy, setStrategy] = useState("fastest");
    const [start_time, setStart_time] = useState("00:00");
    const dispatch = useAppDispatch();
    const {routeData, loading, error} = useAppSelector(state => state.routePlan)
    const cityItemList = cityList.map((city) => {
        return {
            ...city,
            label: city.name
        }
    })

    function disableOption(option: City) {
        return option.name === startCity || option.name === endCity
    }

    function handlePlan(start: string, end: string, strategy: string, start_time: string) {
        dispatch(planRoute({start, end, strategy, start_time}))
    }

    useEffect(() => {
        handlePlan(startCity, endCity, strategy, start_time);
    }, [startCity, endCity, strategy, start_time]);

    return (
        <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
            <h1>Route Plan</h1>
            <div>
                <FormControl>
                    <FormLabel id="demo-radio-buttons-group-label">城市选择</FormLabel>
                    <TextField
                        select
                        label="起始城市"
                        value={startCity}
                        onChange={(event) => setStartCity(event.target.value)}
                        sx={{width: 300}}
                        required
                    >
                        {cityItemList.map((city) => (
                            <MenuItem key={city.name} value={city.name} disabled={disableOption(city)}>
                                {city.name}
                            </MenuItem>
                        ))}
                    </TextField>
                    <div style={{height: 16}}></div>
                    <TextField
                        select
                        label="目标城市"
                        value={endCity}
                        onChange={(event) => setEndCity(event.target.value)}
                        sx={{width: 300}}
                        required
                    >
                        {cityItemList.map((city) => (
                            <MenuItem key={city.name} value={city.name} disabled={disableOption(city)}>
                                {city.name}
                            </MenuItem>
                        ))}
                    </TextField>
                    <div style={{height: 16}}></div>
                    <TextField
                        label="开始时间"
                        type="time"
                        value={start_time}
                        onChange={(event) => setStart_time(event.target.value)}
                        sx={{width: 300}}
                        required
                    />
                </FormControl>
                <div style={{height: 16}}></div>
                <FormControl>
                    <FormLabel id="demo-radio-buttons-group-label">规划策略</FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="demo-radio-buttons-group-label"
                        value={strategy}
                        onChange={(event) => {
                            setStrategy(event.target.value)
                        }}
                        name="radio-buttons-group"
                    >
                        <FormControlLabel value="fastest" control={<Radio/>} label="最快"/>
                        <FormControlLabel value="cheapest" control={<Radio/>} label="最省钱"/>
                        <FormControlLabel value="leastTransfers" control={<Radio/>} label="最少中转"/>
                    </RadioGroup>
                </FormControl>
                <div style={{height: 16}}></div>
                <Button style={{marginTop: 16}} variant="contained"
                        onClick={() => {
                            handlePlan(startCity, endCity, strategy, start_time)
                        }}
                        disabled={!startCity || !endCity}>开始规划</Button>
            </div>
            <div>
                {loading && <div>loading...</div>}
                {error && <div>{error.message}</div>}
                {Boolean(routeData.length) && (
                    <div>
                        <h2>规划结果</h2>
                        <TransportList transports={routeData}/>
                        <p>总耗时：<span>{int2time(time2int(routeData.slice(-1)[0].end_time) - time2int(routeData[0].start_time))}</span>
                        </p>
                        <p>总花费：<span>{routeData.reduce((p, c) => (p + c.price), 0)}￥</span></p>
                    </div>
                )}
            </div>
        </div>
    )
}