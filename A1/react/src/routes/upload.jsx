import { useState } from "react";
import { Form } from "react-router-dom";
import {
  Grid,
  TextField,
  Button,
  Card,
  CardHeader,
  CardContent,
  CardActions,
} from "@mui/material";
import { upload } from "../libs/api";

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  console.log(request, updates);
  const response = await upload(updates);
  return response;
}

export default function Upload() {
  const [filename, setFilename] = useState("Select a file");

  return (
    <Card>
      <CardHeader title="Upload" />
      <Form
        method="POST"
        id="upload-form"
        encType="multipart/form-data"
      >
        <CardContent>
          <Grid container spacing={2}>
          <Grid item xs={12} key="key">
            <TextField
              id="upload-form-key"
              name="key"
              label="Enter a key"
              variant="outlined"
              fullWidth
            />
          </Grid>
          <Grid item xs={12} key="file">
            <Button variant="outlined" component="label" fullWidth>
              {filename}
              <input
                hidden
                accept="image/*"
                type="file"
                name="file"
                onChange={(e) => {
                  setFilename(`Selected: ${e.target.files[0].name}`);
                }}
              />
            </Button>
          </Grid>
          </Grid>
        </CardContent>
        <CardActions>
          <Button size="small" type="submit">
            Submit
          </Button>
        </CardActions>
      </Form>
    </Card>
  );
}

export const UploadRoute = {
  name: "Upload",
  path: "upload",
};
