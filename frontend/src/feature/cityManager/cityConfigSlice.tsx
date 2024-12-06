import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {City} from "../../utils/types";

export const cityConfigSlice = createApi({
    reducerPath: 'cityConfig',
    baseQuery: fetchBaseQuery({baseUrl: '/api/city'}),
    tagTypes: ['CityConfig'],
    endpoints: (builder) => ({
        getCityList: builder.query<City[],void>({
            query: () => '',
            providesTags: ['CityConfig']
        }),
        addCity: builder.mutation<void,string>({
            query: (city: string) => ({
                url: '',
                method: 'POST',
                body: {name: city}
            }),
            invalidatesTags: ['CityConfig']
        }),
        deleteCity: builder.mutation<void,string>({
            query: (city: string) => ({
                url: '',
                method: 'DELETE',
                body: {name: city}
            }),
            invalidatesTags: ['CityConfig']
        })
    })
})

export const {useGetCityListQuery, useAddCityMutation, useDeleteCityMutation} = cityConfigSlice;
