import { useState } from "react";
import {
  useLoaderData,
  Link as RouterLink,
  useNavigate,
  useOutletContext,
} from "react-router-dom";
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  Divider,
  Box,
  Chip
} from "@mui/material";
import LoadingButton from '@mui/lab/LoadingButton';
import ShareIcon from '@mui/icons-material/Share';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import { Tooltip } from "@/components/tooltip";
import {
  retrieveImage,
  deleteImage,
  share
} from "@/libs/api";
import { BasicCard } from "@/components/card";

export async function loader({ params }) {
  const response = await retrieveImage(params.key, params.shareKey);
  if (response.status !== 200) {
    return {
      status: response.status,
      details: {
        message: response.message,
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

  const [bubble, setBubble] = useOutletContext();

  const [image, setImage] = useState(loaderResponse.image[0]);
  const [deleteImageLoading, setDeleteImageLoading] = useState(false);
  const [createShareLoading, setCreateShareLoading] = useState(false);

  let error = null;

  if (loaderResponse) {
    if (loaderResponse.status !== -1 && loaderResponse.status !== 200) {
      error = loaderResponse;
    }
  }

  if (route === PublicRoute.path && !image.share_link) {
    throw new Response("No Found", {
      status: 404,
      statusText: "HTTP Not Found",
    });
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
        image={route === ImageRoute.path ? image.content : image.share_link} // change share linkx
        title={(error && `${error?.status} ${error.details?.statusText}`) || `${image.key}`}
        subheader={
          error ? (error.details?.message) : (
            <>
              {image.tag && route === ImageRoute.path && (
                <Tooltip
                  title="Tag"
                  body={
                    <RouterLink
                      to={`/photos`}
                      state={{ tag: image.tag }}
                    >
                      <Chip
                        label={image.tag}
                        sx={{ mt: 1, mr: 1 }}
                      />
                    </RouterLink>
                  }
                />
              )}
              {image.last_time_accessed && route === ImageRoute.path && (
                <Tooltip
                  title="Last Time Accessed"
                  body={
                    <Chip
                      label={image.last_time_accessed}
                      sx={{ mt: 1, mr: 1 }}
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
                      sx={{ mt: 1, mr: 1 }}
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
                        copyToClipboard(`${window.location.origin}/public/${image.key}`);
                        setBubble({
                          ...bubble,
                          snackbar: {
                            open: true,
                            message: "Link Copied to clipboard"
                          }
                        })
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
                          share(image.key, false).then((response) => {
                            if (response.status === 200) {
                              setImage(response.image[0]);
                              setBubble({
                                ...bubble,
                                snackbar: {
                                  open: true,
                                  message: "Share link deleted"
                                }
                              })
                            } else {
                              setBubble({
                                ...bubble,
                                snackbar: {
                                  open: true,
                                  message: "Failed to delete share link"
                                }
                              })
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
              <LoadingButton
                startIcon={<ShareIcon />}
                size="small"
                loading={createShareLoading}
                loadingPosition="start"
                onClick={() => {
                  setCreateShareLoading(true);
                  share(image.key, true).then((response) => {
                    if (response.status === 200) {
                      setImage(response.image[0]);
                      copyToClipboard(`${window.location.origin}/public/${image.key}`);
                      setBubble({
                        ...bubble,
                        snackbar: {
                          open: true,
                          message: "Share link created and the link is copied to clipboard"
                        }
                      })
                    } else {
                      setBubble({
                        ...bubble,
                        snackbar: {
                          open: true,
                          message: "Failed to create share link"
                        }
                      })
                    }
                    setCreateShareLoading(false);
                  });
                }}
              >
                Create Share
              </LoadingButton>
            )
          ) : (
            <Button
              startIcon={<ShareIcon />}
              size="small"
              onClick={() => {
                copyToClipboard(`${window.location.origin}/public/${image.key}`);
                setBubble({
                  ...bubble,
                  snackbar: {
                    open: true,
                    message: "Link Copied to clipboard"
                  }
                })
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
              <LoadingButton
                color="error"
                size="small"
                loading={deleteImageLoading}
                onClick={() => {
                  setDeleteImageLoading(true);
                  deleteImage(image.key).then((response) => {
                    if (response.status === 200) {
                      navigate("/photos", { replace: true });
                      setBubble({
                        ...bubble,
                        snackbar: {
                          open: true,
                          message: "Image deleted"
                        }
                      })
                    } else {
                      setBubble({
                        ...bubble,
                        snackbar: {
                          open: true,
                          message: "Failed to delete image"
                        }
                      })
                    }
                    setDeleteImageLoading(false);
                  });
                }}
              >
                Delete Image
              </LoadingButton>
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