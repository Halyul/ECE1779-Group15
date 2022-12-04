import { useState, useEffect } from "react";
import {
  useLoaderData,
  Link,
  useNavigate,
} from "react-router-dom";
import WordCloud from 'react-d3-cloud';
import {
  IconButton,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Chip
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { BasicCard } from "@/components/card";
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

export async function action({ params }) {
  return
}


export default function Tag() {
  const navigate = useNavigate();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const loaderResponse = useLoaderData();
  const [tags, setTags] = useState(loaderResponse.data?.tags);

  return (
    <>
      <BasicCard
        title="Tags"
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
                    setTags(response.data?.tags);
                  })
                }}
              >
                <RefreshIcon />
              </IconButton>
            }
          />
        }
        media={
          <WordCloud
            data={tags}
            font="sans-serif"
            width={640}
            height={360}
            fontSize={(word) => Math.sqrt(word.value * 500)}
            spiral="archimedean"
            onWordClick={(event, d) => {
              navigate(`/tag/${d.text}`);
            }}
          />
        }
        content={
          tags && tags.length > 0 ? (
            <List>
              {tags.map((tag) => (
                <ListItem
                  key={tag.text}
                  secondaryAction={
                    <Tooltip
                      title="Count"
                      body={
                        <Chip
                          label={tag.value}
                          size="small"
                        />
                      }
                    />
                  }
                  disablePadding
                >
                  <Link to={`/tag/${tag.text}`} style={{ width: "100%" }}>
                    <ListItemButton>
                      <ListItemText
                        id={tag.text}
                        primary={tag.text}
                      />
                    </ListItemButton>
                  </Link>
                </ListItem>
              )
              )}
            </List>
          ) : (
            <Typography variant="body1">
              No tags found.
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

export const TagRoute = {
  name: "Tag",
  path: "tag/:tag",
};
