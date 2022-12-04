import {
  useState,
  useEffect,
} from "react";
import {
  useLoaderData,
  redirect,
  Link,
} from "react-router-dom";
import {
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
  ListItemButton,
  ListItemAvatar,
  Avatar,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import { retrieveKeys } from "@/libs/api";
import { FormCard } from "@/components/card";
import { Tooltip } from "@/components/tooltip";
import SubmissionPrompt from "@/components/submission-prompt";

export async function loader({ params }) {
  return {
    status: 200,
    data: {
      keys: [
        {
          key: "ajksdfghbuiagda", // the image key
          thumbnail: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
          accesses: 0,
        }
      ]
    }
  };
}

export default function Share() {
  const loaderResponse = useLoaderData();
  const [keyList, setKeyList] = useState(loaderResponse.data?.keys);
  const [isRefreshing, setIsRefreshing] = useState(false);

  return (
    <>
      <FormCard
        id="share_list"
        method="POST"
        title="Shared Images"
        header_action={
          <Tooltip
            title="Refresh"
            body={
              <IconButton
                aria-label="refresh"
                onClick={() => {
                  setIsRefreshing(true);
                  loader({
                    params: {}
                  }).then((response) => {
                    setIsRefreshing(false);
                  })
                }}
              >
                <RefreshIcon />
              </IconButton>
            }
          />

        }
        content={
          keyList && keyList.length > 0 ? (
            <List>
              {keyList.map((key) => (
                <ListItem
                  key={key.key}
                  secondaryAction={
                    <>
                      <Tooltip
                        title="Share"
                        body={
                          <IconButton
                            edge="end"
                            aria-label="share"
                            sx={{ mr: 1 }}
                          >
                            <ShareIcon />
                          </IconButton>
                        }
                      />
                      <Tooltip
                        title="Delete"
                        body={
                          <IconButton
                            edge="end"
                            aria-label="delete"
                          >
                            <DeleteIcon />
                          </IconButton>
                        }
                      />


                    </>
                  }
                  disablePadding
                >
                  <Link to={`/image/${key.key}`} style={{ width: "100%" }}>
                    <ListItemButton>
                      <ListItemAvatar>
                        <Avatar
                          src={`${key.thumbnail}`}
                          variant="square"
                        />
                      </ListItemAvatar>
                      <ListItemText
                        id={key.key}
                        primary={`Key: ${key.key}`}
                        secondary={`Accesses: ${key.accesses}`}
                      />
                    </ListItemButton>
                  </Link>
                </ListItem>
              )
              )}
            </List>
          ) : (
            <Typography variant="body1">
              No keys found.
            </Typography>
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

export const ShareRoute = {
  name: "Share",
  path: "share",
};