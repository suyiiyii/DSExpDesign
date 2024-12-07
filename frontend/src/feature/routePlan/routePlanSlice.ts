import {createAsyncThunk, createSlice, SerializedError} from "@reduxjs/toolkit";
import axios from "axios";

export const planRoute = createAsyncThunk(
    'routePlan/planRoute',
    async ({start, end, strategy}: { start: string, end: string, strategy: string }) => {
        if (!start || !end) {
            throw new Error("start or end is empty");
        }
        const response = await axios.post('/api/routePlan', {start, end, strategy});
        return response.data;
    }
)

const routePlanSlice = createSlice({
    name: 'routePlan',
    initialState: {
        routeData: null,
        loading: false,
        error: null as null | SerializedError
    },
    reducers: {
        resetRouteData(state) {
            state.routeData = null;
        },
    },
    extraReducers: builder => {
        builder.addCase(planRoute.pending, (state) => {
            state.loading = true;
            state.error = null;
        }).addCase(planRoute.fulfilled, (state, action) => {
            state.routeData = action.payload;
            state.loading = false;
        }).addCase(planRoute.rejected, (state, action) => {
            state.loading = false;
            state.error = action.error;
        });
    }
})

export default routePlanSlice.reducer
export const {resetRouteData} = routePlanSlice.actions