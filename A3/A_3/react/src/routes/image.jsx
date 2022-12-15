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
import {
  retrieveImage,
  deleteImage,
  createShare,
  deleteShare,
} from "@/libs/api";
import { BasicCard } from "@/components/card";

export async function loader({ params }) {
  const response = await retrieveImage(params.key, params.shareKey);
  if (response.status !== 200) {
    return {
      status: response.status,
      details: {
        message: response.data.message,
        statusText: response.statusText
      }
    }
  }
  return response;
}

export default function Image({ route }) {
  const loaderResponse = useLoaderData();
  const navigate = useNavigate();

  const [shareMenuAnchorEl, setShareMenuAnchor] = useState(null);
  const shareMenuOpen = Boolean(shareMenuAnchorEl);

  const [snackbarMessage, setSnackbarMessage] = useState(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const [image, setImage] = useState(loaderResponse.data?.image);

  let error = null;

  if (loaderResponse) {
    if (loaderResponse.status !== -1 && loaderResponse.status !== 200) {
      error = loaderResponse;
    }
  }

  const handleShareMenuOpen = (event) => {
    setShareMenuAnchor(event.currentTarget);
  };

  const handleShareMenuClose = () => {
    setShareMenuAnchor(null);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <>
      <BasicCard
        image={image.content}
        title={(error && `${error?.status} ${error.details?.statusText}`) || `${image.key}`}
        subheader={
          error ? (error.details?.message) : (
            <>
              {image.tag && (
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
              )}
              {image.last_time_accessed && (
                <Tooltip
                  title="Last Time Accessed"
                  body={
                    <Chip
                      label={image.last_time_accessed}
                      sx={{ mt: 1, ml: 1 }}
                    />
                  }
                />
              )}
              {image.share_link && (
                <Tooltip
                  title="Number of Access"
                  body={
                    <Chip
                      label={image.number_of_access}
                      sx={{ mt: 1, ml: 1 }}
                    />
                  }
                />
              )}
            </>
          )
        }
        header_action={
          route === ImageRoute.path ? (
            image.share_link ? (
              <>
                <Button
                  aria-controls={shareMenuOpen ? "share-menu" : undefined}
                  aria-haspopup="true"
                  aria-expanded={shareMenuOpen ? "true" : undefined}
                  onClick={handleShareMenuOpen}
                  startIcon={<ShareIcon />}
                  size="small"
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
                  {image.share_link && (
                    <Box>
                      <MenuItem onClick={() => {
                        navigator.clipboard.writeText(image.share_link);
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
                          deleteShare(image.key).then((response) => {
                            if (response.status === 200) {
                              setImage(response.data.image);
                              setSnackbarOpen(true);
                              setSnackbarMessage("Share link deleted");
                            }
                          });
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
                  size="small"
                  onClick={() => {
                    createShare(image.key).then((response) => {
                      if (response.status === 200) {
                        setImage(response.data.image);
                        copyToClipboard(response.data.image.share_link);
                        setSnackbarOpen(true);
                        setSnackbarMessage("Share link created and the link is copied to clipboard");
                      }
                    });
                  }}
              >
                Create Share
              </Button>
            )
          ) : (
            <Button
                startIcon={<ShareIcon />}
                size="small"
                onClick={() => {
                  copyToClipboard(image.share_link);
                  setSnackbarOpen(true);
                  setSnackbarMessage("Link Copied to clipboard");
                }}
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
                color="error"
                size="small"
                onClick={() => {
                deleteImage(image.key).then((response) => {
                  if (response.status === 200) {
                    navigate("/photos", { replace: true });
                  }
                });
              }}
              >
                Delete Image
              </Button>
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