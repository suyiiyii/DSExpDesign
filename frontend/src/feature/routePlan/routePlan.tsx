import {
    Autocomplete,
    Button,
    FormControl,
    FormControlLabel,
    FormLabel,
    Radio,
    RadioGroup,
    TextField
} from "@mui/material";
import React, {useState} from "react";
import {useGetCityListQuery} from "../cityManager/cityConfigSlice";
import {City} from "../../utils/types";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {planRoute} from "./routePlanSlice";
import {TransportList} from "../transportManager/TransportView";

export default function PlanView() {
    const cityList = useGetCityListQuery().data || []
    const [startCity, setStartCity] = useState("");
    const [endCity, setEndCity] = useState("");
    const [strategy, setStrategy] = useState("fastest");
    const dispatch = useAppDispatch();
    const {routeData, loading} = useAppSelector(state => state.routePlan)
    const cityItemList = cityList.map((city) => {
        return {
            ...city,
            label: city.name
        }
    })

    function disableOption(option: City) {
        return option.name === startCity || option.name === endCity
    }

    function handlePlan(start: string, end: string, strategy: string) {
        console.log(start, end, strategy)
        dispatch(planRoute({start, end, strategy}))

    }

    return (
        <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
            <h1>Route Plan</h1>
            <div>
                <FormControl>
                    <FormLabel id="demo-radio-buttons-group-label">城市选择</FormLabel>
                    <Autocomplete
                        disablePortal
                        options={cityItemList}
                        sx={{width: 300}}
                        renderInput={(params) => <TextField {...params} label="起始城市"/>}
                        onChange={(event, value) => {
                            setStartCity(value ? value.label : "")
                        }}
                        getOptionDisabled={disableOption}
                    />
                    <div style={{height: 16}}></div>
                    <Autocomplete
                        disablePortal
                        options={cityItemList}
                        sx={{width: 300}}
                        renderInput={(params) => <TextField {...params} label="目标城市"/>}
                        onChange={(event, value) => {
                            setEndCity(value ? value.label : "")
                        }}
                        getOptionDisabled={disableOption}
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
                            handlePlan(startCity, endCity, strategy)
                        }}
                        disabled={!startCity || !endCity}>开始规划</Button>
            </div>
            <div>
                {loading && <div>loading...</div>}
                {routeData && (
                    <div>
                        <h2>规划结果</h2>
                        <TransportList transports={routeData}/>
                    </div>
                )}
            </div>
        </div>
    )
}