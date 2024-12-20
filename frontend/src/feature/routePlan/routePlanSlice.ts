import {createAsyncThunk, createSlice, SerializedError} from "@reduxjs/toolkit";
import axios from "axios";
import {PlanResult, Transport} from "../../utils/types";
import {selectDataset} from "../../utils/datasetSlice";
import {RootState} from "../../app/store";

export const planRoute = createAsyncThunk(
    'routePlan/planRoute',
    async ({start, end, strategy, start_time}: {
        start: string,
        end: string,
        strategy: string,
        start_time: string
    }, thunkAPI): Promise<PlanResult> => {
        if (!start || !end) {
            throw new Error("start or end is empty");
        }
        const state = thunkAPI.getState() as RootState;
        const dataset = selectDataset(state);
        const response = await axios.post('/api/routePlan', {
            start,
            end,
            strategy,
            start_time
        }, {headers: {Dataset: dataset}});
        return response.data;
    }
)

const routePlanSlice = createSlice({
    name: 'routePlan',
    initialState: {
        routeData: [] as Transport[],
        total_price: 0,
        total_time: 0,
        loading: false,
        pathMap: "",
        error: null as null | SerializedError
    },
    reducers: {
        resetRouteData(state) {
            state.routeData = [];
        },
    },
    extraReducers: builder => {
        builder.addCase(planRoute.pending, (state) => {
            state.loading = true;
            state.error = null;
        }).addCase(planRoute.fulfilled, (state, action) => {
            state.routeData = action.payload.path;
            state.total_price = action.payload.total_price;
            state.total_time = action.payload.total_time;
            state.pathMap = action.payload.pathMap;
            state.loading = false;
            state.error = null;
        }).addCase(planRoute.rejected, (state, action) => {
            state.routeData = [];
            state.loading = false;
            state.error = action.error;
        });
    }
})

export default routePlanSlice.reducer
export const {resetRouteData} = routePlanSlice.actions