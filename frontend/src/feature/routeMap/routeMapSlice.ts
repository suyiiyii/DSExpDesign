import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

export const routeMapSlice = createApi({
    reducerPath: 'routeMap',
    baseQuery: fetchBaseQuery({baseUrl: '/api/routeMap'}),
    tagTypes: ['RouteMap'],
    endpoints: (builder) => ({
        getRouteMap: builder.query<{data: string}, void>({
            query: () => '',
            providesTags: ['RouteMap']
        })
    })
})

export const {useGetRouteMapQuery} = routeMapSlice;