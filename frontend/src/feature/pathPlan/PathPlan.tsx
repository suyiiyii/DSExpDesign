import {Autocomplete, TextField} from "@mui/material";
import React from "react";
import {useGetCityListQuery} from "../cityManager/cityConfigSlice";


export function PlanView() {
    const cityList = useGetCityListQuery().data || []
    const cityItemList = cityList.map((city) => {
        return {
            label: city.name
        }
    })
    return (
        <div>
            <Autocomplete
                disablePortal
                options={cityItemList}
                sx={{width: 300}}
                renderInput={(params) => <TextField {...params} label="起始城市"/>}
            />
            <Autocomplete
                disablePortal
                options={cityItemList}
                sx={{width: 300}}
                renderInput={(params) => <TextField {...params} label="目标城市"/>}
            />
        </div>
    )
}