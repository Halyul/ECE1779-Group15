import {
  useState,
  useMemo
} from "react";
import {
  useLoaderData,
  useOutletContext,
} from "react-router-dom";
import {
  CardMedia,
  Button,
  IconButton,
  Radio,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
} from "@mui/material";
import LoadingButton from '@mui/lab/LoadingButton';
import RefreshIcon from "@mui/icons-material/Refresh";
import {
  retrieveKeys,
  deleteImage,
  deleteShare,
} from "@/libs/api";
import SubmissionPrompt from "@/components/submission-prompt";
import DataTable from "@/components/data-table";

export async function loader({ params }) {
  const response = await retrieveKeys(true);
  if (response.status !== 200) {
    return {
      status: response.status,
      statusText: response.statusText
    }
  }
  return response;
}

export default function Images() {
  const loaderResponse = useLoaderData();
  const [bubble, setBubble] = useOutletContext();
  const [imagesList, setImagesList] = useState(loaderResponse.data.images);
  const [selectionModel, setSelectionModel] = useState([imagesList[0].key]);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const [deleteImageLoading, setDeleteImageLoading] = useState(false);
  const [deleteShareLoading, setDeleteShareLoading] = useState(false);

  const selectedImage = useMemo(() => {
    const image = imagesList.find((image) => image.key === selectionModel[0]);
    return {
      image,
      mapping: [
        { name: "User", value: image.user },
        { name: "Key", value: image.key },
        { name: "Tag", value: image.tag },
        { name: "Shared", value: image.share_link ? true : false },
        { name: "Number of Access", value: image.number_of_access },
        { name: "Last Time Accessed", value: image.last_time_accessed },
      ]
    }
  }, [imagesList, selectionModel]);

  const columns = useMemo(
    () => [
      {
        field: "radiobutton",
        headerName: "",
        flex: 0.25,
        sortable: false,
        filterable: false,
        renderCell: (params) => (
          <Radio checked={selectionModel[0] === params.id} value={params.id} />
        )
      },
      { field: "user", headerName: "User", flex: 0.5, },
      { field: "key", headerName: "Key", flex: 1, },
      { field: "tag", headerName: "Tag", flex: 0.5, },
      { field: "share_link", headerName: "Shared", type: "boolean", flex: 0.25, },
    ],
    [selectionModel],
  );

  const refreshList = () => {
    setIsRefreshing(true);
    loader({
      params: {}
    }).then((response) => {
      setIsRefreshing(false);
      setImagesList(response.data?.images);
      setSelectionModel([imagesList[0].key]);
    })
  }

  return (
    <>
      <DataTable
        title="Images"
        header_action={
          <IconButton
            aria-label="refresh"
            onClick={() => {
              refreshList()
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        columns={columns}
        rows={imagesList}
        isRefreshing={isRefreshing}
        getRowId={(r) => r.key}
        selectionModel={selectionModel}
        onSelectionModelChange={(newSelectionModel) => {
          setSelectionModel(newSelectionModel);
        }}
        content={
          <>
            <CardMedia component="img"
              image={selectedImage.image.thumbnail}
              sx={{ marginTop: "8px" }}
            />
            <TableContainer>
              <Table>
                <TableBody>
                  {selectedImage.mapping.map((row) => (
                    <TableRow
                      key={row.name}
                      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {row.name}
                      </TableCell>
                      {row.value === undefined && console.log(row.value)}
                      <TableCell align="right">{(row.value).toString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </>
        }
        actions={
          <>
            <LoadingButton
              color="error"
              size="small"
              loading={deleteImageLoading}
              onClick={() => {
                setDeleteImageLoading(true);
                deleteImage(selectedImage.image.key, true).then((response) => {
                  if (response.status === 200) {
                    const result = imagesList.filter((image) => image.key !== selectedImage.image.key)
                    setImagesList(result)
                    setSelectionModel([result[0].key]);
                    setBubble({...bubble, snackbarOpen: true, snackbarMessage: "Image deleted"})
                  } else {
                    setBubble({...bubble, snackbarOpen: true, snackbarMessage: "Failed to delete image"})
                  }
                  setDeleteImageLoading(false);
                });
              }}
            >
              Delete Image
            </LoadingButton>
            {
              selectedImage.image.share_link && (
                <LoadingButton
                  color="error"
                  size="small"
                  loading={deleteShareLoading}
                  onClick={() => {
                    setDeleteShareLoading(true);
                    deleteShare(selectedImage.image.key, true).then((response) => {
                      if (response.status === 200) {
                        const result = imagesList.map((image) => image.key === selectedImage.image.key ? response.data.image : image
                        )
                        setImagesList(result);
                        setBubble({...bubble, snackbarOpen: true, snackbarMessage: "Share link deleted"})
                      } else {
                        setBubble({...bubble, snackbarOpen: true, snackbarMessage: "Failed to delete share link"})
                      }
                      setDeleteShareLoading(false);
                    });
                  }}
                >
                  Delete Share
                </LoadingButton>
              )
            }
          </>
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

export const ImagesRoute = {
  name: "Images",
  path: "images",
};