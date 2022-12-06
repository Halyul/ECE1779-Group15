import { useState, useEffect } from "react";
import { useLoaderData } from "react-router-dom";
import {
  Box,
  Typography,
  IconButton,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { DataGrid } from "@mui/x-data-grid";
import { BasicCard } from "@/components/card";
// import { getStatus } from "@/libs/api";
import SubmissionPrompt from "@/components/submission-prompt";

const columns = [
  { field: "name", headerName: "Name", flex: 0.5 },
  { field: "value", headerName: "Value", flex: 1 },
];


export async function loader({ params }) {
  // const response = await getStatus();
  return {
    status: 200,
    data: {
      stats: [
        { name: 'Jon', value: true },
        { name: 'Cersei', value: 42 },
        { name: 'Jaime', value: 45 },
        { name: 'Arya', value: 16 },
        { name: 'Daenerys', value: null },
        { name: "lol", value: 150 },
        { name: 'Ferrara', value: 44 },
        { name: 'Rossini', value: 36 },
        { name: 'Harvey', value: 65 },
      ]
    }
  };
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
          statsList.length > 0 ? (
            <Box sx={{ height: "61.8vh", maxHeight: 768 }}>
              <DataGrid
                getRowId={(r) => r.name}
                rows={statsList}
                columns={columns}
                disableSelectionOnClick />
            </Box>
          ) : (
            <Typography variant="body1">No stats found.</Typography>
          )
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