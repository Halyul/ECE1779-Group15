import { useState, useMemo } from "react";
import {
  useLoaderData,
  useNavigate,
  useLocation,
} from "react-router-dom";
import { GridActionsCellItem } from '@mui/x-data-grid';
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
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import PreviewIcon from '@mui/icons-material/Preview';
import { retrieveKeys } from "@/libs/api";
import { BasicCard } from "@/components/card";
import SubmissionPrompt from "@/components/submission-prompt";
import DataTable from "@/components/data-table";

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
          is_shared: true,
        },
        {
          key: "gura", // the image key
          thumbnail: "https://gura.ch/images/0.jpg",
          tag: "nan",
          is_shared: false,
        },
        {
          key: "78", // the image key
          thumbnail: "https://gura.ch/images/404.jpg",
          tag: "nan",
          is_shared: true,
        },
        {
          key: "8", // the image key
          thumbnail: "https://gura.ch/images/200.jpg",
          tag: "nan",
          is_shared: false,
        },
        {
          key: "12381", // the image key
          thumbnail: "https://gura.ch/images/302.jpg",
          tag: "nan",
          is_shared: true,
        },
        {
          key: Math.random().toString(), // the image key
          thumbnail: "https://gura.ch/images/414.jpg",
          tag: "nan",
          is_shared: false,
        }
      ]
    }
  };
}

export default function Photos() {
  const loaderResponse = useLoaderData();
  const location = useLocation();
  const navigate = useNavigate();
  const filteredTag = location.state?.tag || null;
  const [keyList, setKeyList] = useState(loaderResponse.data?.keys);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectionModel, setSelectionModel] = useState(
    filteredTag ?
      keyList.filter((image) => image.tag === filteredTag).map((image) => image.key) :
      keyList.map((image) => image.key)
  );
  const selectedImages = useMemo(() => {
    return keyList.filter((image) => selectionModel.includes(image.key));
  }, [keyList, selectionModel]);

  const columns = [
    { field: "key", headerName: "Key", flex: 1, },
    { field: "tag", headerName: "Tag", flex: 0.5, },
    { field: "is_shared", headerName: "Shared", type: "boolean", flex: 0.25, },
  ];

  return (
    <>
      <DataTable
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
                setSelectionModel(response.data?.keys.map((image) => { return image.key }));
              })
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        columns={columns}
        rows={keyList}
        isRefreshing={isRefreshing}
        getRowId={(r) => r.key}
        selectionModel={selectionModel}
        onSelectionModelChange={(newSelectionModel) => {
          setSelectionModel(newSelectionModel);
        }}
        checkboxSelection
        initialState={{
          filter: {
            filterModel: {
              items: [{ columnField: "tag", operatorValue: "contains", value: filteredTag }],
            },
          },
        }}
        content={
          selectedImages && selectedImages.length > 0 ? (
            <ImageList cols={window.innerWidth > 768 ? 3 : (window.innerWidth > 500 ? 2 : 1)} gap={8} variant="masonry">
              {selectedImages.map((key) => (
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
                  />
                </ImageListItem>
              ))}
            </ImageList>
          ) : (
            <Typography variant="body1">
              No photo selected.
            </Typography>
          )
        }
      />
      <SubmissionPrompt
        failed={{
          title: "Failed to retrieve photos",
          text: loaderResponse?.statusText,
        }}
        submitting={{
          text: "Retrieving...",
          open: isRefreshing,
          setOpen: setIsRefreshing,
        }}
        submittedText="Photos retrieved successfully"
        submissionStatus={loaderResponse}
      />
    </>
  );
}

export const PhotosRoute = {
  name: "Photos",
  path: "photos",
};
