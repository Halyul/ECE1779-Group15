import { useState } from "react";
import {
  useLoaderData,
  Form
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

export async function loader({ params }) {
  if (!params.key) {
    return null;
  }
  // const image = await getImage(params.imageKey);
  // return image;
  return {
    key: params.key,
    content: "https://mui.com/static/images/cards/contemplative-reptile.jpg",
  };
}

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  console.log(updates);
  // await updateContact(params.contactId, updates);
}

export default function Image() {
  const image = useLoaderData();
  // TODO: use dialog to show progress
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(false);

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
            name="image_key"
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
