import React from "react";
import {Divider, IconButton, List, ListItem, ListItemText} from "@mui/material";
import {useGetTransportListQuery} from "./transportConfigSlice";
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

function TransportView() {
    const transportList = useGetTransportListQuery().data || [];
    console.log(transportList);
    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <h1>Transport View</h1>
            <List sx={style}>
                {transportList.map((transport, index) => (
                    <React.Fragment key={transport.name}>
                        <ListItem
                            secondaryAction={
                                <IconButton edge="end" aria-label="delete">
                                    <DeleteIcon/>
                                </IconButton>
                            }
                        >
                            <ListItemText primary={`${transport.start} --${transport.name}-> ${transport.end}`}/>
                        </ListItem>
                        {index !== transportList.length - 1 && (
                            <Divider component="li"/>
                        )}
                    </React.Fragment>
                ))}
            </List>
        </div>
    );
}

export default TransportView; 