import {
  useState
} from "react";
import {
  useLoaderData,
  Form,
  redirect
} from "react-router-dom";
import {
  Card,
  CardHeader,
  CardActions,
  CardContent,
  CardMedia,
  Button,
  TextField
} from "@mui/material";
import { retrieveImage } from "../libs/api";

export async function loader({ params }) {
  const response = await retrieveImage(params.key);
  if (response.status !== 200) {
    throw new Response(response.data.message, {
      status: response.status,
      statusText: response.statusText,
    });
  }
  return {
    content: response.data.content,
    key: params.key,
  };
}

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  return redirect(`/image/${updates.key}`);
}

export default function Image() {
  const image = useLoaderData();

  return (
    <Card>
      {image && (
        <CardMedia
          component="img"
          image={image.content}
          alt={image.key}
        />
      )}
      <CardHeader
        title="Image Key"
        subheader={(image && image.key)|| "No key is presented. Please provide a key."}
      />
      <Form method="POST" id="image-form">
        <CardContent>
          <TextField
            id="image-text-field"
            name="key"
            label="Enter an image key"
            variant="outlined"
            fullWidth
          />
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

export const ImageRoute = {
  name: "Image",
  path: "image",
};

export const ImageWithKeyRoute = {
  name: "Image with Key",
  path: "image/:key",
};
