import {
  useState,
  useMemo
} from "react";
import {
  useLoaderData,
} from "react-router-dom";
import {
  Button,
  IconButton,
  Radio,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { retrieveKeys } from "@/libs/api";
import SubmissionPrompt from "@/components/submission-prompt";
import DataTable from "@/components/data-table";
import {
  BasicCard
} from "@/components/card";

export async function loader({ params }) {
  // const response = await getStatus();
  return {
    status: 200,
    data: {
      images: [
        { key: "1", user: 'Jon', tag: "test", is_shared: true, number_of_access: 1, last_time_accessed: "27/11/2022 19:19:36" },
        { key: "2", user: 'Doe', tag: "123", is_shared: false, number_of_access: 1, last_time_accessed: "27/11/2022 19:19:36" },
      ]
    }
  };
}

export default function Images() {
  const loaderResponse = useLoaderData();
  const [imagesList, setImagesList] = useState(loaderResponse.data.images);
  const [selectionModel, setSelectionModel] = useState([imagesList[0].key]);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const selectedImage = useMemo(() => {
    const image = imagesList.find((image) => image.key === selectionModel[0]);
    return {
      image,
      src: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
      mapping: [
        { name: "User", value: image.user },
        { name: "Key", value: image.key },
        { name: "Tag", value: image.tag },
        { name: "Shared", value: image.is_shared },
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
      { field: "user", headerName: "User", flex: 1, },
      { field: "key", headerName: "Key", flex: 1, },
      { field: "tag", headerName: "Tag", flex: 0.5, },
      { field: "is_shared", headerName: "Shared", type: "boolean", flex: 0.25, },
    ],
    [selectionModel],
  );

  return (
    <>
      <DataTable
        title="Images"
        header_action={
          <IconButton
            aria-label="refresh"
            onClick={() => {
              setIsRefreshing(true);
              loader({
                params: {}
              }).then((response) => {
                setIsRefreshing(false);
                setImagesList(response.data?.images);
              })
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
        children={
          <BasicCard
            image={selectedImage.src}
            actions={
              <>
                <Button
                  color="error"
                >
                  Delete Image
                </Button>
                {
                  selectedImage.image.is_shared && (
                    <Button
                      color="error"
                    >
                      Delete Share
                    </Button>
                  )
                }
              </>
            }
            content={
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
                        <TableCell align="right">{(row.value).toString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            }
            sx={{
              maxWidth: "unset",
            }}
          />
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