import { useState, useEffect } from "react";
import {
  useLoaderData,
  Link,
} from "react-router-dom";
import {
  IconButton,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemAvatar,
  Avatar,
  Chip
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { BasicCard } from "@/components/card";
import { Tooltip } from "@/components/tooltip";
import SubmissionPrompt from "@/components/submission-prompt";

export async function loader({ params }) {
  return {
    tag: params.tag,
    status: 200,
    data: {
      images: [
        {
          key: "ajksdfghbuiagda", // the image key
          thumbnail: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
          accesses: 0,
        }
      ]
    }
  };
}

export default function Tag() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const loaderResponse = useLoaderData();
  const tag = loaderResponse.tag;
  const [images, setImages] = useState(loaderResponse.data?.images);

  return (
    <>
      <BasicCard
        title={`Tag: ${tag}`}
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
                    setImages(response.data?.images);
                  })
                }}
              >
                <RefreshIcon />
              </IconButton>
            }
          />
        }
        content={
          images && images.length > 0 ? (
            <List>
              {images.map((image) => (
                <ListItem
                  key={image.key}
                  disablePadding
                >
                  <Link to={`/image/${image.key}`} style={{ width: "100%" }}>
                  <ListItemButton>
                      <ListItemAvatar>
                        <Avatar
                          src={image.thumbnail}
                          variant="square"
                        />
                      </ListItemAvatar>
                      <ListItemText
                        id={image.key}
                        primary={image.key}
                      />
                    </ListItemButton>
                  </Link>
                </ListItem>
              )
              )}
            </List>
          ) : (
            <Typography variant="body1">
              No images found.
            </Typography>
          )
        }
      />
      <SubmissionPrompt
        failed={{
          title: "Failed to retrieve images",
          text: loaderResponse?.statusText,
        }}
        submitting={{
          text: "Retrieving...",
          open: isRefreshing,
          setOpen: setIsRefreshing,
        }}
        submittedText="Images retrieved successfully"
        submissionStatus={loaderResponse}
      />
    </>
  );
}

export const TagRoute = {
  name: "Tag",
  path: "tag/:tag",
};
