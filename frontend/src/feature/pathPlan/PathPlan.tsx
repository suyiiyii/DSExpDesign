import {Autocomplete, TextField} from "@mui/material";
import React from "react";

const cityList = [
    {
        "label": "上海"
    },
    {
        "label": "北京"
    },
    {
        "label": "广州"
    },
    {
        "label": "深圳"
    },
    {
        "label": "厦门"
    },
    {
        "label": "杭州"
    },
    {
        "label": "天津"
    },
    {
        "label": "重庆"
    },
    {
        "label": "香港"
    },
    {
        "label": "澳门"
    },
    {
        "label": "武汉"
    },
    {
        "label": "长沙"
    },
    {
        "label": "济南"
    },
    {
        "label": "哈尔滨"
    },
    {
        "label": "西安"
    }
]

export function PlanView() {
    return (
        <div>
            <Autocomplete
                disablePortal
                options={cityList}
                sx={{width: 300}}
                renderInput={(params) => <TextField {...params} label="起始城市"/>}
            />
            <Autocomplete
                disablePortal
                options={cityList}
                sx={{width: 300}}
                renderInput={(params) => <TextField {...params} label="目标城市"/>}
            />
        </div>
    )
}