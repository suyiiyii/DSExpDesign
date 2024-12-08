import React, {useState} from "react";
import {Divider, IconButton, List, ListItem, ListItemText, TextField} from "@mui/material";
import {useAddCityMutation, useGetCityListQuery} from "./cityConfigSlice";
import DeleteIcon from '@mui/icons-material/Delete';
import {LoadingButton} from "@mui/lab";


const style = {
    py: 0,
    width: '100%',
    maxWidth: 360,
    borderRadius: 2,
    border: '1px solid',
    borderColor: 'divider',
    backgroundColor: 'background.paper',
};

function CityView() {
    const cityList = useGetCityListQuery().data || []
    const [cityName, setCityName] = useState("");
    const [addCity] = useAddCityMutation();
    const [loading, setLoading] = useState(false);

    function doAddCity(cityName: string) {
        setLoading(true);
        addCity(cityName).unwrap().then(() => {
            setCityName("");
        }).finally(() => {
            setLoading(false);
        })
    }

    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <h1>City View</h1>
            <List sx={style}>
                {cityList.map((city, index) => (
                    <React.Fragment key={city.name}>
                        <ListItem
                            secondaryAction={
                                <IconButton edge="end" aria-label="delete">
                                    <DeleteIcon/>
                                </IconButton>
                            }
                        >
                            <ListItemText primary={city.name}/>
                        </ListItem>
                        {index !== cityList.length - 1 && (
                            <Divider component="li"/>
                        )}
                    </React.Fragment>
                ))}
            </List>
            <div>
                <h2>添加城市</h2>
                <div style={{display: "flex", alignItems: "flex-end"}}>
                    <TextField id="standard-basic" label="城市名称" variant="standard" value={cityName}
                               onChange={(event) => {
                                   setCityName(event.target.value)
                               }}/>
                    <LoadingButton variant="contained" style={{marginLeft: 8}} loading={loading} onClick={() => {
                        doAddCity(cityName);
                    }}>提交</LoadingButton>
                </div>
            </div>
        </div>
    );
}

export default CityView;