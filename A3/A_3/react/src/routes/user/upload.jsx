import {
  useState,
  useEffect
} from "react";
import {
  useActionData,
  Link,
  useLocation,
} from "react-router-dom";
import {
  Grid,
  TextField,
  Button,
} from "@mui/material";
import { upload } from "@/libs/api";
import { FormCard } from "@/components/card";
import SubmissionPrompt from "@/components/submission-prompt";
import { TooltipOnError } from "@/components/tooltip";

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  const response = await upload(updates);
  return {
    status: response.status,
    statusText: response.statusText,
  };
}

export default function Upload() {
  const actionResponse = useActionData();
  const location = useLocation();
  const [isReupload, setIsReupload] = useState(location.state?.image ? true : false);
  const [filename, setFilename] = useState("Select a file");
  const [image, setImage] = useState(location.state?.image.content);
  const [keyValue, setKeyValue] = useState(location.state?.image.key || "");
  const [submitted, setSubmitted] = useState(false);
  const [keyError, setKeyError] = useState(false);
  const [fileError, setFileError] = useState(false);
  const [navigateToUploaded, setNavigateToUploaded] = useState(false);

  useEffect(() => {
    if (actionResponse) {
      if (actionResponse.status === 200) {
        setNavigateToUploaded(true);
      }
    }
  }, [actionResponse]);

  return (
    <>
      <FormCard
        image={image}
        id="upload"
        method="POST"
        encType="multipart/form-data"
        onSubmit={(e) => {
          setSubmitted(true);
        }}
        title={isReupload ? "Reupload an Image" : "Upload an Image"}
        content={
          <Grid container spacing={2}>
            <Grid item xs={12} key="key">
              <TooltipOnError
                open={keyError}
                handleClose={() => setKeyError(false)}
                title="Please enter a key, spaces are NOT allowed. More than 48 characters are NOT allowed."
                body={
                  <TextField
                    id="upload-form-key"
                    name="key"
                    label="Enter a key"
                    variant="outlined"
                    fullWidth
                    error={keyError}
                    value={keyValue}
                    disabled={isReupload}
                    onChange={(e) => {
                      if (e.target.value.includes(" ") || e.target.value.length > 48) {
                        setKeyError(true);
                      } else {
                        setKeyValue(e.target.value);
                        setKeyError(false);
                      }
                    }}
                  />
                }
              />
            </Grid>
            <Grid item xs={12} key="file">
              <TooltipOnError
                open={fileError}
                handleClose={() => setFileError(false)}
                title="Please select a file"
                body={
                  <Button
                    variant="outlined"
                    component="label"
                    fullWidth
                    color={fileError ? "error" : "primary"}
                  >
                    {filename}
                    <input
                      hidden
                      accept="image/*"
                      type="file"
                      name="file"
                      onChange={(e) => {
                        if (e.target.files.length > 0) {
                          setFilename(`Selected: ${e.target.files[0].name}`);
                          setImage(URL.createObjectURL(e.target.files[0]));
                          setFileError(false);
                        } else {
                          setFilename("Select a file");
                          setImage(null);
                          setFileError(true);
                        }
                      }}
                    />
                  </Button>
                }
              />
            </Grid>
          </Grid>
        }
        actions={
          <>
            <Button
              size="small"
              type="submit"
              onClick={(e) => {
                if (keyValue === "" || keyValue.includes(" ") || keyValue.length > 48) {
                  setKeyError(true);
                  e.preventDefault();
                }
                if (filename === "Select a file") {
                  setFileError(true);
                  e.preventDefault();
                }
              }}
            >
              Submit
            </Button>
            {navigateToUploaded ? (
              <Link
                to={`/image/${keyValue}`}
                style={{
                  marginLeft: "auto",
                }}
              >
                <Button
                  size="small"
                >
                  Take a look
                </Button>
              </Link>
            ) : (
              <Button
                size="small"
                onClick={() => {
                  setImage(null)
                  setFilename("Select a file")
                  setKeyValue("")
                  setIsReupload(false)
                }}
                style={{
                  marginLeft: "auto",
                }}
              >
                Reset
              </Button>
            )}
          </>

        }
      >

      </FormCard>
      <SubmissionPrompt
        failed={{
          title: "Failed to upload the image",
          text: actionResponse?.statusText,
        }}
        submitting={{
          text: "Image is uploading...",
          open: submitted,
          setOpen: setSubmitted,
        }}
        submittedText="Image uploaded successfully"
        submissionStatus={actionResponse}
      />
    </>
  );
}

export const UploadRoute = {
  name: "Upload",
  path: "upload",
};
