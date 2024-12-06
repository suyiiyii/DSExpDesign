import {configureStore} from "@reduxjs/toolkit";
import {cityConfigSlice} from "../feature/cityManager/cityConfigSlice";


export const store = configureStore({
    reducer: {
        [cityConfigSlice.reducerPath]: cityConfigSlice.reducer,
    },
    middleware: (getDefaultMiddleware) => {
        return getDefaultMiddleware()
            .prepend(cityConfigSlice.middleware)
            .concat(cityConfigSlice.middleware)
    }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
export type AppStore = typeof store
