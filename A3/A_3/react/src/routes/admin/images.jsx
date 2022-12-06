import {
  useState,
} from "react";
import {
  useLoaderData,
  Link,
} from "react-router-dom";
import {
  Box,
  IconButton,
  Typography,
  Radio,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import { DataGrid } from "@mui/x-data-grid";
import { retrieveKeys } from "@/libs/api";
import { BasicCard } from "@/components/card";
import { Tooltip } from "@/components/tooltip";
import SubmissionPrompt from "@/components/submission-prompt";
// https://codesandbox.io/s/hrf09?file=/src/App.js
const columns = [
  { field: "name", headerName: "Name", flex: 0.5 },
  { field: "value", headerName: "Value", flex: 1, type: "boolean" },
];

export async function loader({ params }) {
  // const response = await getStatus();
  return {
    status: 200,
    data: {
      stats: [
        { name: 'Jon', value: true },
        { name: 'Cersei', value: true },
        { name: 'Jaime', value: false },
        { name: 'Arya', value: false },
        { name: 'Daenerys', value: false },
        { name: "lol", value: true },
        { name: 'Ferrara', value: true },
        { name: 'Rossini', value: false },
        { name: 'Harvey', value: false },
      ]
    }
  };
}

export default function Images() {
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
                checkboxSelection
                loading={isRefreshing}
              />
            </Box>
          ) : (
            <Typography variant="body1">No stats found.</Typography>
          )
        }
      />
      <SubmissionPrompt
        failed={{
          title: "Failed to retrieve keys",
          text: loaderResponse?.statusText,
        }}
        submitting={{
          text: "Retrieving...",
          open: isRefreshing,
          setOpen: setIsRefreshing,
        }}
        submittedText="Key retrieved successfully"
        submissionStatus={loaderResponse}
      />
    </>

  );
}

export const ImagesRoute = {
  name: "Images",
  path: "images",
};