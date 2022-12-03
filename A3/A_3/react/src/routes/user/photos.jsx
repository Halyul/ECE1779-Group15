import { useState, useEffect } from "react";
import {
  useLoaderData,
  useNavigate,
} from "react-router-dom";
import {
  Box,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
  ImageList,
  ImageListItem,
  ImageListItemBar,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import ShareIcon from '@mui/icons-material/Share';
import { retrieveKeys } from "@/libs/api";
import { FormCard } from "@/components/card";
import SubmissionPrompt from "@/components/submission-prompt";

export async function loader({ params }) {
  const response = await retrieveKeys();
  if (response.status !== 200) {
    return {
      status: response.status,
      statusText: response.statusText
    }
  }
  // return response;
  return {
    status: 200,
    data: {
      keys: [
        {
          key: "ajksdfghbuiagda", // the image key
          thumbnail: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
          tag: "test",
          isShared: true,
        },
        {
          key: "aaa8", // the image key
          thumbnail: "https://gura.ch/images/0.jpg",
          tag: "nan",
          isShared: false,
        },
        {
          key: "78", // the image key
          thumbnail: "https://gura.ch/images/404.jpg",
          tag: "nan",
          isShared: true,
        },
        {
          key: "8", // the image key
          thumbnail: "https://gura.ch/images/200.jpg",
          tag: "nan",
          isShared: false,
        },
        {
          key: "12381", // the image key
          thumbnail: "https://gura.ch/images/302.jpg",
          tag: "nan",
          isShared: true,
        },
        {
          key: "1", // the image key
          thumbnail: "https://gura.ch/images/414.jpg",
          tag: "nan",
          isShared: false,
        }
      ]
    }
  };
}

export async function action({ request, params }) {
  return;
}

export default function Photos() {
  const loaderResponse = useLoaderData();
  const navigate = useNavigate();
  const [keyList, setKeyList] = useState(loaderResponse.data?.keys);
  const [isRefreshing, setIsRefreshing] = useState(false);

  return (
    <>
      <FormCard
        id="photos"
        method="POST"
        title="Photos"
        header_action={
          <IconButton
            aria-label="refresh"
            type="submit"
            onClick={() => {
              setIsRefreshing(true);
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        content={
          keyList && keyList.length > 0 ? (
            <ImageList cols={window.innerWidth > 768 ? 3 : (window.innerWidth > 500 ? 2 : 1)} gap={8} variant="masonry">
              {keyList.map((key) => (
                <ImageListItem key={key.key}>
                  <img
                    src={key.thumbnail}
                    alt={key.tag}
                    loading="lazy"
                    onClick={() => {
                      navigate(`/image/${key.key}`);
                    }}
                    style={{ cursor: "pointer" }}
                  />
                  <ImageListItemBar
                    title={key.key}
                    subtitle={key.tag}
                    actionIcon={
                      key.isShared && (
                        <IconButton
                          sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                        >
                          <ShareIcon />
                        </IconButton>
                      )}
                  />
                </ImageListItem>
              ))}
            </ImageList>
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

export const PhotosRoute = {
  name: "Photos",
  path: "photos",
};
