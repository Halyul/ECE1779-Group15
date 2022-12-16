import { useState, useEffect } from "react";
import { useLoaderData } from "react-router-dom";
import {
  Box,
  IconButton,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { DataGrid } from "@mui/x-data-grid";
import { BasicCard } from "@/components/card";
import { getStats } from "@/libs/api";
import SubmissionPrompt from "@/components/submission-prompt";

const columns = [
  { field: "name", headerName: "Name", flex: 0.5 },
  { field: "value", headerName: "Value", flex: 1 },
];


export async function loader({ params }) {
  const response = await getStats();
  return response;
}

export default function Stats() {
  const loaderResponse = useLoaderData();
  const [statsList, setStatsList] = useState(loaderResponse.data.stats);
  const [isRefreshing, setIsRefreshing] = useState(false);

  return (
    <>
      <BasicCard
        title="Stats"
        header_action={
          <IconButton
            aria-label="refresh"
            onClick={() => {
              setIsRefreshing(true);
              loader({
                params: {}
              }).then((response) => {
                setIsRefreshing(false);
                setStatsList(response.data?.stats);
              })
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        content={
          <Box sx={{ height: "61.8vh", maxHeight: 768 }}>
            <DataGrid
              getRowId={(r) => r.name}
              loading={isRefreshing}
              rows={statsList}
              columns={columns}
              disableSelectionOnClick />
          </Box>
        }
      />
      <SubmissionPrompt
        failed={{
          title: "Failed to retrieve stats",
          text: loaderResponse?.statsText,
        }}
        submitting={{
          text: "Retrieving...",
          open: isRefreshing,
          setOpen: setIsRefreshing,
        }}
        submittedText="Stats retrieved successfully"
        submissionStatus={loaderResponse}
      />
    </>
  );
}

export const StatsRoute = {
  name: "Stats",
  path: "stats",
};