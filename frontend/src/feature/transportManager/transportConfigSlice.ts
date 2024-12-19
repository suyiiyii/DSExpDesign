import {createApi} from "@reduxjs/toolkit/query/react";
import {Transport} from "../../utils/types";
import {dynamicQuery} from "../../utils/query";


export const transportConfigSlice = createApi({
    reducerPath: 'transportConfig',
    baseQuery: dynamicQuery,
    tagTypes: ['TransportConfig'],
    endpoints: (builder) => ({
        getTransportList: builder.query<Transport[],void>({
            query: () => '/transport',
            providesTags: ['TransportConfig']
        }),
        addTransport: builder.mutation<void,Transport>({
            query: (transport: Transport) => ({
                url: '/transport',
                method: 'POST',
                body: transport
            }),
            invalidatesTags: ['TransportConfig']
        }),
        deleteTransport: builder.mutation<void,Transport>({
            query: (transport: Transport) => ({
                url: '/transport/delete',
                method: 'POST',
                body: transport
            }),
            invalidatesTags: ['TransportConfig']
        })
    })
})

export const {useGetTransportListQuery, useAddTransportMutation, useDeleteTransportMutation} = transportConfigSlice;