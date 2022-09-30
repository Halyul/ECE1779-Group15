import { useState, useEffect } from "react";
import { useLoaderData, NavLink } from "react-router-dom";
import {
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography
} from "@mui/material";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import { retrieveKeys } from "../libs/api";
import { RefreshCard } from "../components/card";
import SubmissionPrompt from "../components/submission-prompt";

export async function loader({ params }) {
  const response = await retrieveKeys();
  return response;
}

export async function action({ request, params }) {
  return;
}

export default function Keys() {
  const loaderResponse = useLoaderData();
  const [keyList, setKeyList] = useState(loaderResponse.data.keys);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    setIsRefreshing(false);
    setKeyList(loaderResponse.data.keys);
  }, [loaderResponse]);

  return (
    <>
      <RefreshCard
        title="Keys"
        body={
          keyList ? (
            <List>
            {keyList.map((key) => (
              <ListItem
                key={key}
                secondaryAction={
                  <NavLink to={`../image/${key}`}>
                    <IconButton
                      edge="end"
                      aria-label={`Go to image with key ${key}`}
                    >
                      <NavigateNextIcon />
                    </IconButton>
                  </NavLink>
                }
              >
                <ListItemText primary={key} />
              </ListItem>
            ))}
            </List>
          ) : (
            <Typography variant="body1">
              No keys found.
            </Typography>
          )
        }
        handleOnClick={() => {
          setIsRefreshing(true);
        }}
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
        submissionStatus = {loaderResponse}
      />
    </>
  );
}

export const KeysRoute = {
  name: "Keys",
  path: "keys",
};
