import {configureStore} from "@reduxjs/toolkit";
import {cityConfigSlice} from "../feature/cityManager/cityConfigSlice";
import { transportConfigSlice } from "../feature/transportManager/transportConfigSlice";
import {routeMapSlice} from "../feature/routeMap/routeMapSlice";


export const store = configureStore({
    reducer: {
        [cityConfigSlice.reducerPath]: cityConfigSlice.reducer,
        [transportConfigSlice.reducerPath]: transportConfigSlice.reducer,
        [routeMapSlice.reducerPath]: routeMapSlice.reducer
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
