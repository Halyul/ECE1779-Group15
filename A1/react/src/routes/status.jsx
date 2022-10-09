import { useState, useEffect } from "react";
import { useLoaderData } from "react-router-dom";
import { Box, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { RefreshCard } from "../components/card";
import { getStatus } from "../libs/api";
import SubmissionPrompt from "../components/submission-prompt";

const columns = [
  { field: "name", headerName: "Name", flex: 0.5 },
  { field: "value", headerName: "Value", flex: 1 },
];

export async function loader({ params }) {
  const response = await getStatus();
  return response;
}

export async function action({ request, params }) {
  return;
}

export default function Status() {
  const loaderResponse = useLoaderData();
  const [statusList, setStatusList] = useState(loaderResponse.data.status);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    setIsRefreshing(false);
    setStatusList(loaderResponse.data.status);
  }, [loaderResponse]);
  return (
    <>
      <RefreshCard
        title="Status"
        body={
          statusList.length > 0 ? (
            <Box sx={{ height: "61.8vh", maxHeight: 768 }}>
              <DataGrid
                getRowId={(r) => r.name}
                rows={statusList}
                columns={columns}
                disableSelectionOnClick />
            </Box>
          ) : (
            <Typography variant="body1">No status found.</Typography>
          )
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
