import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {Transport} from "../utils/types";


export const transportConfigSlice = createApi({
    reducerPath: 'transportConfig',
    baseQuery: fetchBaseQuery({baseUrl: '/api/transport'}),
    tagTypes: ['TransportConfig'],
    endpoints: (builder) => ({
        getTransportList: builder.query<Transport[],void>({
            query: () => '',
            providesTags: ['TransportConfig']
        }),
        addTransport: builder.mutation<void,Transport>({
            query: (transport: Transport) => ({
                url: '',
                method: 'POST',
                body: transport
            }),
            invalidatesTags: ['TransportConfig']
        }),
        deleteTransport: builder.mutation<void,Transport>({
            query: (transport: Transport) => ({
                url: '',
                method: 'DELETE',
                body: transport
            }),
            invalidatesTags: ['TransportConfig']
        })
    })
})

export const {useGetTransportListQuery, useAddTransportMutation, useDeleteTransportMutation} = transportConfigSlice;