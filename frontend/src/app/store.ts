import {configureStore} from "@reduxjs/toolkit";
import {cityConfigSlice} from "../feature/cityManager/cityConfigSlice";
import {transportConfigSlice} from "../feature/transportManager/transportConfigSlice";
import {routeMapSlice} from "../feature/routeMap/routeMapSlice";
import routePlanSliceReducer from "../feature/routePlan/routePlanSlice";
import datasetSliceReducer from "../utils/datasetSlice";


export const store = configureStore({
    reducer: {
        [cityConfigSlice.reducerPath]: cityConfigSlice.reducer,
        [transportConfigSlice.reducerPath]: transportConfigSlice.reducer,
        [routeMapSlice.reducerPath]: routeMapSlice.reducer,
        routePlan: routePlanSliceReducer,
        dataset: datasetSliceReducer
    },
    middleware: (getDefaultMiddleware) => {
        return getDefaultMiddleware()
            .concat(cityConfigSlice.middleware)
            .concat(transportConfigSlice.middleware)
            .concat(routeMapSlice.middleware)
    }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
export type AppStore = typeof store
