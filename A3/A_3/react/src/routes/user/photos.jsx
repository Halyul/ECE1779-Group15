import { useState, useEffect } from "react";
import {
  useLoaderData,
  useNavigate,
} from "react-router-dom";
import {
  IconButton,
  Typography,
  ImageList,
  ImageListItem,
  ImageListItemBar,
  Tooltip,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import ShareIcon from '@mui/icons-material/Share';
import { retrieveKeys } from "@/libs/api";
import { BasicCard } from "@/components/card";
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
          key: "gura", // the image key
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
          key: Math.random().toString(), // the image key
          thumbnail: "https://gura.ch/images/414.jpg",
          tag: "nan",
          isShared: false,
        }
      ]
    }
  };
}

export default function Photos() {
  const loaderResponse = useLoaderData();
  const navigate = useNavigate();
  const [keyList, setKeyList] = useState(loaderResponse.data?.keys);
  const [isRefreshing, setIsRefreshing] = useState(false);

  return (
    <>
      <BasicCard
        id="photos"
        title="Photos"
        header_action={
          <IconButton
            aria-label="refresh"
            onClick={() => {
              setIsRefreshing(true);
              loader({
                params: {}
              }).then((response) => {
                setIsRefreshing(false);
                setKeyList(response.data?.keys);
              })
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        content={
          keyList && keyList.length > 0 ? (
            <ImageList cols={window.innerWidth > 768 ? 3 : (window.innerWidth > 500 ? 2 : 1)} gap={8} variant="masonry">
              {keyList.map((key) => (
                <ImageListItem
                  key={key.key}
                  style={{ cursor: "pointer" }}
                  onClick={() => {
                      navigate(`/image/${key.key}`);
                    }}
                >
                  <img
                    src={key.thumbnail}
                    alt={key.tag}
                    loading="lazy"
                  />
                  <ImageListItemBar
                    title={key.key}
                    subtitle={key.tag}
                    actionIcon={
                      key.isShared && (
                        <Tooltip title="Shared">
                        <IconButton
                          sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                        >
                          <ShareIcon />
                          </IconButton>
                        </Tooltip>
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
