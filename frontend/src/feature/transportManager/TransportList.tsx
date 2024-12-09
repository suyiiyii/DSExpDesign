import {Transport} from "../../utils/types";
import {Divider, IconButton, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import React from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import TrainIcon from "@mui/icons-material/Train";
import FlightIcon from "@mui/icons-material/Flight";

const style = {
    py: 0,
    width: '100%',
    maxWidth: 360,
    borderRadius: 2,
    border: '1px solid',
    borderColor: 'divider',
    backgroundColor: 'background.paper',
};

export function TransportList({transports, doDelete}: {
    transports: Transport[],
    doDelete?: (transport: Transport) => void
}) {
    return (
        <List sx={style}>
            {transports.map((transport, index) => (
                <React.Fragment key={JSON.stringify(transport)}>
                    <ListItem
                        secondaryAction={
                            doDelete && (
                                <IconButton edge="end" aria-label="delete" onClick={() => {
                                    doDelete(transport)
                                }}>
                                    <DeleteIcon/>
                                </IconButton>)
                        }
                    >
                        <ListItemIcon>
                            {transport.type === 'train' ? <TrainIcon/> : <FlightIcon/>}
                        </ListItemIcon>
                        <div>
                            <ListItemText primary={`${transport.start} --${transport.name}-> ${transport.end}`}/>
                            <p>
                                {`${transport.start_time} - ${transport.end_time}`}
                            </p>
                        </div>
                    </ListItem>
                    {index !== transports.length - 1 && (
                        <Divider component="li"/>
                    )}
                </React.Fragment>
            ))}
        </List>
    );
}