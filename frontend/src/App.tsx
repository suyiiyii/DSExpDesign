import React from "react";
import "./App.css";
import {Box, MenuItem, Tab, Tabs, TextField} from "@mui/material";
import PlanView from "./feature/routePlan/RoutePlan";
import {store} from "./app/store";
import {Provider} from "react-redux";
import CityView from "./feature/cityManager/CityView";
import TransportView from "./feature/transportManager/TransportView";
import RouteMapView from "./feature/routeMap/RouteMapView";
import AltRouteIcon from '@mui/icons-material/AltRoute';
import LocationCityIcon from '@mui/icons-material/LocationCity';
import EmojiTransportationIcon from '@mui/icons-material/EmojiTransportation';
import RouteIcon from '@mui/icons-material/Route';
import {useAppDispatch, useAppSelector} from "./app/hooks";
import {selectDataset, setDataset} from "./utils/datasetSlice";
import {transportConfigSlice} from "./feature/transportManager/transportConfigSlice";
import {cityConfigSlice} from "./feature/cityManager/cityConfigSlice";
import {routeMapSlice} from "./feature/routeMap/routeMapSlice";
import {resetRouteData} from "./feature/routePlan/routePlanSlice";

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
    const [value, setValue] = React.useState(1);

    function handleChange(event: React.SyntheticEvent, newValue: number) {
        setValue(newValue);
    }

    function DatasetSelect() {
        const dataset = useAppSelector(selectDataset)
        const dispatch = useAppDispatch()

        function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
            dispatch(setDataset(event.target.value))
            // 重置当前的数据
            dispatch(cityConfigSlice.util.resetApiState())
            dispatch(transportConfigSlice.util.resetApiState())
            dispatch(resetRouteData())
            dispatch(routeMapSlice.util.resetApiState())

        }

        return (
            <TextField
                select
                label="数据选择"
                name="数据选择"
                value={dataset}
                onChange={handleChange}
                required
            >

                <MenuItem value="full">Full</MenuItem>
                <MenuItem value="exp1">Exp1</MenuItem>
                <MenuItem value="exp2">Exp2</MenuItem>
            </TextField>
        )
    }

    return (
        <Provider store={store}>
            <div className="App">
                <Box sx={{borderBottom: 1, borderColor: "divider"}}>
                    <Tabs
                        value={value}
                        onChange={handleChange}
                        aria-label="basic tabs example"
                    >
                        <div style={{marginTop: 10, width: 80}}>
                            <DatasetSelect/>
                        </div>
                        <Tab label="路径规划" icon={<AltRouteIcon />} iconPosition={"start"}/>
                        <Tab label="地点查询" icon={<LocationCityIcon />} iconPosition={"start"}/>
                        <Tab label="路线查询" icon={<EmojiTransportationIcon />} iconPosition={"start"}/>
                        <Tab label="路线图" icon={<RouteIcon/>} iconPosition={"start"}/>
                    </Tabs>
                </Box>
                <CustomTabPanel value={value} index={1}>
                    <PlanView/>
                </CustomTabPanel>
                <CustomTabPanel value={value} index={2}>
                    <CityView/>
                </CustomTabPanel>
                <CustomTabPanel value={value} index={3}>
                    <TransportView/>
                </CustomTabPanel>
                <CustomTabPanel value={value} index={4}>
                    <RouteMapView/>
                </CustomTabPanel>
            </div>
        </Provider>
    );
}

export default App;
