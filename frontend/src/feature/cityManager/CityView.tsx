import React, {useState} from "react";
import {Divider, IconButton, List, ListItem, ListItemText, TextField} from "@mui/material";
import {useAddCityMutation, useDeleteCityMutation, useGetCityListQuery} from "./cityConfigSlice";
import DeleteIcon from '@mui/icons-material/Delete';
import {LoadingButton} from "@mui/lab";
import {enqueueSnackbar, SnackbarProvider} from "notistack";
import {ResultStatus} from "../../utils/types";


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
    const [deleteCity] = useDeleteCityMutation();
    const [loading, setLoading] = useState(false);

    function doAddCity(cityName: string) {
        if (cityName === "") {
            enqueueSnackbar("城市名称不能为空", {variant: "error"});
            return;
        }
        if (cityList.find(city => city.name === cityName)) {
            enqueueSnackbar("城市已存在", {variant: "error"});
            return;
        }
        setLoading(true);
        addCity(cityName).unwrap().then(() => {
            setCityName("");
        }).finally(() => {
            setLoading(false);
        })
    }

    function doDeleteCity(cityName: string) {
        deleteCity(cityName).unwrap().then((payload) => {
                const value = payload as unknown as ResultStatus;
                if (value.status === "error") {
                    enqueueSnackbar("删除失败 " + value.msg, {variant: "error"});
                    return;
                }
                enqueueSnackbar("删除成功 " + value.msg, {variant: "success"});
            }
        )
    }

    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <SnackbarProvider/>
            <h1>City View</h1>
            <List sx={style}>
                {cityList.map((city, index) => (
                    <React.Fragment key={city.name}>
                        <ListItem
                            secondaryAction={
                                <IconButton edge="end" aria-label="delete" onClick={() => {
                                    doDeleteCity(city.name)
                                }}>
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