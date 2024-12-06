import React from 'react';
import './App.css';
import {Box, Tab, Tabs} from "@mui/material";
import {PlanView} from "./feature/pathPlan/PathPlan";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function CustomTabPanel(props: TabPanelProps) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{p: 3}}>{children}</Box>}
        </div>
    );
}


function App() {
    const [value, setValue] = React.useState(0);

    function handleChange(event: React.SyntheticEvent, newValue: number) {
        setValue(newValue);
    }

    return (
        <div className="App">
            <Box sx={{borderBottom: 1, borderColor: 'divider'}}>
                <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="路径规划"/>
                    <Tab label="地点查询"/>
                    <Tab label="路线查询"/>
                </Tabs>
            </Box>
            <CustomTabPanel value={value} index={0}>
                <PlanView/>
            </CustomTabPanel>
            <CustomTabPanel value={value} index={1}>
                Item Two
            </CustomTabPanel>
            <CustomTabPanel value={value} index={2}>
                Item Three
            </CustomTabPanel>
        </div>
    );
}

export default App;
