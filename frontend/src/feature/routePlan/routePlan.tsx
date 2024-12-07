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

export default function PlanView() {
    const cityList = useGetCityListQuery().data || []
    const [startCity, setStartCity] = useState("");
    const [endCity, setEndCity] = useState("");

    const cityItemList = cityList.map((city) => {
        return {
            ...city,
            label: city.name
        }
    })

    function disableOption(option: City) {
        return option.name === startCity || option.name === endCity
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
                        defaultValue="female"
                        name="radio-buttons-group"
                    >
                        <FormControlLabel value="female" control={<Radio/>} label="最快"/>
                        <FormControlLabel value="male" control={<Radio/>} label="最省钱"/>
                        <FormControlLabel value="other" control={<Radio/>} label="最少中转"/>
                    </RadioGroup>
                </FormControl>
                <div style={{height: 16}}></div>
                <Button style={{marginTop: 16}} variant="contained">开始规划</Button>
            </div>
        </div>
    )
}