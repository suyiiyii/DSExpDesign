export interface City {
    name: string;
}

export interface Transport {
    type: string;
    name: string;
    start: string;
    end: string;
    price: number;
    start_time: string;
    end_time: string;
    run_id: string;
}

export interface PlanResult {
    path: Transport[];
    total_price: number;
    total_time: number;
}

export interface ResultStatus {
    status: string;
    msg: string;
}