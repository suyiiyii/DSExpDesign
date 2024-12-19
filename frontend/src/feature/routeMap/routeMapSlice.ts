import {createApi} from "@reduxjs/toolkit/query/react";
import {dynamicQuery} from "../../utils/query";

export const routeMapSlice = createApi({
    reducerPath: 'routeMap',
    baseQuery: dynamicQuery,
    tagTypes: ['RouteMap'],
    endpoints: (builder) => ({
        getRouteMap: builder.query<{data: string}, void>({
            query: () => '/routeMap',
            providesTags: ['RouteMap']
        })
    })
})

export const {useGetRouteMapQuery} = routeMapSlice;