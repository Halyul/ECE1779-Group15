import { useState, useEffect } from "react";
import { useLoaderData } from "react-router-dom";
import { Box, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { RefreshCard } from "../components/card";
import SubmissionPrompt from "../components/submission-prompt";
import ReactEcharts from "echarts-for-react";

const columns = [
  { field: "name", headerName: "Name", flex: 0.5 },
  { field: "value", headerName: "Value", flex: 1 },
];

export async function loader({ params }) {
  // const response = await getStatus();
  // return response;
}

export async function action({ request, params }) {
  return;
}

export default function Status() {
  // const loaderResponse = useLoaderData();
  // const [statusList, setStatusList] = useState(loaderResponse.data.status);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // useEffect(() => {
  //   setIsRefreshing(false);
  //   setStatusList(loaderResponse.data.status);
  // }, [loaderResponse]);
  return (
    <>
      <RefreshCard
        title="Status"
        subtitle="The status changes in last 10 minutes of the system"
        body={
          <ReactEcharts
      option={{
        title: {
          text: 'Steps',
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        dataZoom: [
          {
            type: 'slider',
            show: true,
            xAxisIndex: [0],
            start: 1,
            end: 12
          },
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: ['2021-10-09', '2021-10-10', '2021-10-11', '2021-10-12', '2021-10-13', '2021-10-14', '2021-10-15', '2021-10-16', '2021-10-17', '2021-10-18', '2021-10-19', '2021-10-20', '2021-10-21', '2021-10-22', '2021-10-23', '2021-10-24', '2021-10-25', '2021-10-26', '2021-10-27', '2021-10-28', '2021-10-29', '2021-10-30', '2021-10-31', '2021-11-01', '2021-11-02', '2021-11-03', '2021-11-04', '2021-11-05', '2021-11-06', '2021-11-07', '2021-11-08', '2021-11-09', '2021-11-10', '2021-11-11', '2021-11-12', '2021-11-13', '2021-11-14', '2021-11-15', '2021-11-16', '2021-11-17', '2021-11-18', '2021-11-19', '2021-11-20', '2021-11-21', '2021-11-22', '2021-11-23', '2021-11-24', '2021-11-25', '2021-11-26' ]
        },
        yAxis: {
          type: 'value', 
          axisLabel: {
            formatter: '{value} Steps'
          },
        },
        series: [
          {
            data: [4168, 12441, 3297, 2801, 5465, 5609, 3907, 3487, 2967, 4988, 3620, 3648, 3635, 7262, 2138, 2177, 3431, 3424, 5990, 5262, 3882, 10322, 4370, 2621, 4715, 2951, 8873, 7002, 3711, 2692, 3106, 5574, 3381, 3430, 3492, 4225, 2738, 2048, 4196, 6041, 2918, 2366, 3848, 7078, 3129, 2387, 3252, 2626, 6399],
            type: 'line'
          }
        ]
        }}
      />
        }
      />
      {/* <SubmissionPrompt
        failed={{
          title: "Failed to retrieve status",
          text: loaderResponse?.statusText,
        }}
        submitting={{
          text: "Retrieving...",
          open: isRefreshing,
          setOpen: setIsRefreshing,
        }}
        submittedText="Status retrieved successfully"
        submissionStatus = {loaderResponse}
      /> */}
    </>
  );
}

export const StatusRoute = {
  name: "Status",
  path: "status",
};
