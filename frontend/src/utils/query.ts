import {fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {selectDataset} from "./datasetSlice";

export const dynamicQuery = async (args: any, api: any, extraOptions: any) => {
    const state = api.getState()
    const dataset = selectDataset(state)
    const rawBaseQuery = fetchBaseQuery({baseUrl: '/api', headers: {Dataset: dataset}})
    return rawBaseQuery(args, api, extraOptions)
}