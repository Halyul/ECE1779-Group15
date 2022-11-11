import { useState, useEffect } from "react";
import {
  useLoaderData,
  useActionData
} from "react-router-dom";
import { RefreshCard } from "../components/card";
import SubmissionPrompt from "../components/submission-prompt";
import { getStatus } from "../libs/api";
import ECharts from "../components/echarts";

export async function loader({ params }) {
  const response = await getStatus();
  if (response.status !== 200) {
    throw new Response(response.data.message, {
      status: response.status,
      statusText: response.statusText,
    });
  }
  return response;
}

export async function action({ request, params }) {
  return;
}

export default function Status() {
  const loaderResponse = useLoaderData();
  const [statusList, setStatusList] = useState(loaderResponse.data.content);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    setIsRefreshing(false);
    setStatusList(loaderResponse.data.content);
  }, [loaderResponse]);

  const generateXAxis = (length) => {return Array.from(Array(length).keys()).map((i) => {return i + 1}).reverse()}

  return (
    <>
      <RefreshCard
        title="Status"
        subtitle="The status changes in last 30 minutes of the system"
        body={
          <>
            <ECharts
              title="Hit and Miss Rate"
              xAxis={[
                {
                  type: 'category',
                  boundaryGap: false,
                  data: generateXAxis(statusList.hit_rate.length),
                }
              ]}
              yAxis={[
                {
                  type: 'value',
                  axisLabel: {
                    formatter: '{value} %'
                  },
                }]
              }
              series={[
                {
                  name: 'Hit Rate',
                  data: statusList.hit_rate,
                  type: 'line',
                  smooth: true,
                },
                {
                  name: 'Miss Rate',
                  data: statusList.miss_rate,
                  type: 'line',
                  smooth: true,
                }
              ]}
            />
            <ECharts
              title="Number of Items in Cache"
              xAxis={[
                {
                  type: 'category',
                  boundaryGap: false,
                  data: generateXAxis(statusList.number_of_items_in_cache.length)
                }
              ]}
              yAxis={[
                {
                  type: 'value',
                }
              ]}
              series={[
                {
                  data: statusList.number_of_items_in_cache,
                  type: 'line'
                }
              ]}
            />
            <ECharts
              title="Total Size of Items"
              xAxis={[
                {
                  type: 'category',
                  boundaryGap: false,
                  data: generateXAxis(statusList.total_size_of_items_in_cache.length)
                }
              ]}
              yAxis={[
                {
                  type: 'value',
                  axisLabel: {
                    formatter: '{value} MB'
                  },
                }]
              }
              series={[
                {
                  data: statusList.total_size_of_items_in_cache,
                  type: 'line'
                }
              ]}
            />
            <ECharts
              title="Number of Requests Served"
              xAxis={[
                {
                  type: 'category',
                  boundaryGap: false,
                  data: generateXAxis(statusList.number_of_requests_served_per_minute.length)
                }
              ]}
              yAxis={[
                {
                  type: 'value',
                }]
              }
              series={[
                {
                  data: statusList.number_of_requests_served_per_minute,
                  type: 'line'
                }
              ]}
            />
          </>
        }
      />
      <SubmissionPrompt
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
      />
    </>
  );
}

export const StatusRoute = {
  name: "Status",
  path: "status",
};
