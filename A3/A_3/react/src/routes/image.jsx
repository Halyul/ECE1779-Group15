import { useState } from "react";
import {
  useLoaderData,
  redirect,
  NavLink,
} from "react-router-dom";
import {
  Button,
  TextField,
} from "@mui/material";
import { retrieveImage } from "@/libs/api";
import { FormCard } from "@/components/card";
import { TooltipOnError } from "@/components/tooltip";

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
  return {
    status: 200,
    image: {
      content: response.data.content,
      key: params.key,
    }
  };
}

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  return redirect(`/image/${updates.key}`);
}

export async function publicAction({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  return redirect(`/public/${updates.key}`);
}

export default function Image({route}) {
  const loaderResponse = useLoaderData();
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

  return (
      <FormCard
        id="image"
        method="POST"
        title={(error && `${error?.status} ${error.details?.statusText}`) || (route === ImageRoute.path ? "Image Key" : "Share Key")}
        subheader={
          (image && image.key) || (error && error.details?.message) || "Key is not presented. Please provide a key."
        }
        image={image}
      content={
        <>
          <TooltipOnError
            open={keyError}
            handleClose={() => setKeyError(false)}
            title="Please enter a key wihtout spaces. More than 48 characters are NOT allowed."
            body={
              <TextField
                id="image-text-field"
                name="key"
                label={
                  ((image || error) && "Enter another key") || "Enter an key"
                }
                variant="outlined"
                fullWidth
                error={keyError}
                value={keyValue}
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
          </>
          
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
              }}
            >
              Submit
            </Button>
            {image && route === ImageRoute.path && (
              <NavLink
                to={`../upload/?key=${image.key}`}
                style={{
                  marginLeft: "auto",
                }}
              >
                <Button size="small">Re-upload</Button>
              </NavLink>
            )}
          </>
        }
      />
  );
}

export const ImageRoute = {
  name: "Image with Key",
  path: "image/:key",
};

export const PublicRoute = {
  name: "Public",
  path: "public",
};

export const PublicWithShareKeyRoute = {
  name: "Public with Share Key",
  path: "public/:shareKey",
};