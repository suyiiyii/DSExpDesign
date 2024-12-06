import React from "react";
import {Divider, IconButton, List, ListItem, ListItemText} from "@mui/material";
import {useGetCityListQuery} from "./cityConfigSlice";
import DeleteIcon from '@mui/icons-material/Delete';


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
    console.log(cityList)
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
        </div>
    );
}

export default CityView;