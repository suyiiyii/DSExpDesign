import React from "react";
import {Divider, IconButton, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import {useGetTransportListQuery} from "./transportConfigSlice";
import DeleteIcon from '@mui/icons-material/Delete';
import TrainIcon from '@mui/icons-material/Train';
import FlightIcon from '@mui/icons-material/Flight';
import {Transport} from "../../utils/types";

const style = {
    py: 0,
    width: '100%',
    maxWidth: 360,
    borderRadius: 2,
    border: '1px solid',
    borderColor: 'divider',
    backgroundColor: 'background.paper',
};

export function TransportList({transports}:{transports: Transport[]}) {
    return (
        <List sx={style}>
            {transports.map((transport, index) => (
                <React.Fragment key={JSON.stringify(transport)}>
                    <ListItem
                        secondaryAction={
                            <IconButton edge="end" aria-label="delete">
                                <DeleteIcon/>
                            </IconButton>
                        }
                    >
                        <ListItemIcon>
                            {transport.type === 'train' ? <TrainIcon/> : <FlightIcon/>}
                        </ListItemIcon>
                        <ListItemText primary={`${transport.start} --${transport.name}-> ${transport.end}`}/>
                    </ListItem>
                    {index !== transports.length - 1 && (
                        <Divider component="li"/>
                    )}
                </React.Fragment>
            ))}
        </List>
    );

}

function TransportView() {
    const transportList = useGetTransportListQuery().data || [];
    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <h1>Transport View</h1>
            <TransportList transports={transportList}/>
        </div>
    );
}

export default TransportView; 