import {createApi} from "@reduxjs/toolkit/query/react";
import {City} from "../../utils/types";
import {dynamicQuery} from "../../utils/query";

export const cityConfigSlice = createApi({
    reducerPath: 'cityConfig',
    baseQuery: dynamicQuery,
    tagTypes: ['CityConfig'],
    endpoints: (builder) => ({
        getCityList: builder.query<City[],void>({
            query: () => '/city',
            providesTags: ['CityConfig']
        }),
        addCity: builder.mutation<void,string>({
            query: (city: string) => ({
                url: '/city',
                method: 'POST',
                body: {name: city}
            }),
            invalidatesTags: ['CityConfig']
        }),
        deleteCity: builder.mutation<void,string>({
            query: (city: string) => ({
                url: '/city/delete',
                method: 'POST',
                body: {name: city}
            }),
            invalidatesTags: ['CityConfig']
        })
    })
})

export const {useGetCityListQuery, useAddCityMutation, useDeleteCityMutation} = cityConfigSlice;
