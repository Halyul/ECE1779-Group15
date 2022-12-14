import { useState } from "react";
import {
  useLoaderData,
  Link as RouterLink,
  useNavigate,
} from "react-router-dom";
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  Divider,
  Box,
  Snackbar,
  Chip
} from "@mui/material";
import ShareIcon from '@mui/icons-material/Share';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import { Tooltip } from "@/components/tooltip";
import { retrieveImage } from "@/libs/api";
import { BasicCard } from "@/components/card";

export async function loader({ params }) {
  // const response = await retrieveImage(params.key, params.shareKey);
  // if (response.status !== 200) {
  //   return {
  //     status: response.status,
  //     details: {
  //       message: response.data.message,
  //       statusText: response.statusText
  //     }
  //   }
  // }
  // return {
  //   status: 200,
  //   image: {
  //     content: response.data.content,
  //     key: params.key,
  //   }
  // };
  return [
    {
      status: 200,
      image: {
        content: "https://gura.ch/images/0.jpg",
        key: "gura",
        tag: "nan",
        shard_link: "123"
      }
    },
    {
      status: 200,
      image: {
        content: "https://gura.ch/images/404.jpg",
        key: "gura",
        tag: "test",
        shard_link: null
      }
    }
  ][Math.floor(Math.random() * 2)];
}

export default function Image({ route }) {
  const loaderResponse = useLoaderData();
  const navigate = useNavigate();

  const [shareMenuAnchorEl, setShareMenuAnchor] = useState(null);
  const shareMenuOpen = Boolean(shareMenuAnchorEl);

  const [snackbarMessage, setSnackbarMessage] = useState(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const [keyError, setKeyError] = useState(false);
  const [keyValue, setKeyValue] = useState("");
  let image = null;
  let error = null;

  if (loaderResponse) {
    if (loaderResponse.status === 200) {
      image = loaderResponse.image;
    } else if (loaderResponse.status !== -1) {
      error = loaderResponse;
    }
  }

  const handleShareMenuOpen = (event) => {
    setShareMenuAnchor(event.currentTarget);
  };

  const handleShareMenuClose = () => {
    setShareMenuAnchor(null);
  };

  return (
    <>
      <BasicCard
        image={image.content}
        title={(error && `${error?.status} ${error.details?.statusText}`) || `Key: ${image.key}`}
        subheader={
          error ? (error.details?.message) : (
            image.tag ? (
              <Tooltip
                title="Tag"
                body={
                  <RouterLink
                    to={`/photos`}
                    state={{ tag: image.tag }}
                  >
                    <Chip
                      label={image.tag}
                      sx={{ mt: 1 }}
                    />
                  </RouterLink>
                }
              />
            ) : ("")
          )
        }
        header_action={
          route === ImageRoute.path ? (
            image.shard_link ? (
              <>
                <Button
                  aria-controls={shareMenuOpen ? "share-menu" : undefined}
                  aria-haspopup="true"
                  aria-expanded={shareMenuOpen ? "true" : undefined}
                  onClick={handleShareMenuOpen}
                  startIcon={<ShareIcon />}
                >
                  Manage Share
                </Button>
                <Menu
                  id="share-menu"
                  anchorEl={shareMenuAnchorEl}
                  open={shareMenuOpen}
                  onClose={handleShareMenuClose}
                  MenuListProps={{
                    "aria-labelledby": "basic-button",
                  }}
                  anchorOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  transformOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                >
                  {image.shard_link && (
                    <Box>
                      <MenuItem onClick={() => {
                        navigator.clipboard.writeText(image.shard_link);
                        setSnackbarOpen(true);
                        setSnackbarMessage("Link Copied to clipboard");
                        handleShareMenuClose()
                      }}>
                        <ListItemIcon>
                          <ContentCopyIcon fontSize="small" />
                        </ListItemIcon>
                        Copy
                      </MenuItem>
                      <MenuItem
                        onClick={() => {
                          handleShareMenuClose();
                        }}
                      >
                        <ListItemIcon>
                          <DeleteIcon fontSize="small" />
                        </ListItemIcon>
                        Delete
                      </MenuItem>
                    </Box>
                  )}
                  <Divider sx={{ my: 0.5 }} />
                  <MenuItem onClick={handleShareMenuClose}>
                    <ListItemIcon>
                      <CloseIcon fontSize="small" />
                    </ListItemIcon>
                    Close
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <Button
                startIcon={<ShareIcon />}
              >
                Create Share
              </Button>
            )
          ) : (
            <Button
              startIcon={<ShareIcon />}
            >
              Copy Link
            </Button>
          )
        }
        actions={
          route === ImageRoute.path && (
            <>
              <RouterLink
                to={`/upload`}
                state={{ image: image }}
              >
                <Button size="small">Re-upload</Button>
              </RouterLink>
              <Button
                size="small"
                style={{
                  marginLeft: "auto",
                }}
                onClick={() => {
                  navigate(-1, { replace: true });
                }}
              >
                Back
              </Button>
            </>
          )
        }
      />
      <Snackbar
        open={snackbarOpen}
        message={snackbarMessage}
        autoHideDuration={6000}
        onClose={() => { setSnackbarOpen(false) }}
      />
    </>
  );
}

export const ImageRoute = {
  name: "Image with Key",
  path: "image/:key",
};

export const PublicRoute = {
  name: "Public",
  path: "public/:shareKey",
};