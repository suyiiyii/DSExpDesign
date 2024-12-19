import {createSlice} from "@reduxjs/toolkit";

export interface datasetState {
    dataset: string;
    datasetOptions: string[];
}

const initialState: datasetState = {
    dataset: "full",
    datasetOptions: ["full", "sample"],
}

const datasetSlice = createSlice({
    name: 'dataset',
    initialState,
    reducers: {
        setDataset(state, action) {
            state.dataset = action.payload;
        }
    }
})

export const {setDataset} = datasetSlice.actions
export const selectDataset = (state: { dataset: datasetState }) => state.dataset.dataset

export default datasetSlice.reducer