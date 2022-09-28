import { useState } from "react";
import { Form } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardActions,
  CardContent,
  MenuItem,
  Button,
  TextField,
  Grid
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

export default function Config() {
  const [policy, setPolicy] = useState("");

  return (
    <Card>
      <CardHeader title="Configuration" />
      <Form method="POST" id="config-form">
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                id="config-form-capacity"
                name="capacity"
                label="Capacity in MB"
                variant="outlined"
                value=""
                fullWidth
                inputProps={{
                  inputMode: "numeric",
                  pattern: "[0-9]*",
                }}
                type="number"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                id="config-form-policy"
                name="policy"
                label="Replacement Policy"
                variant="outlined"
                value={policy}
                fullWidth
                select
                onChange={(event) => {
                  setPolicy(event.target.value);
                }}
              >
                <MenuItem key="rr" value="rr">
                  Random Replacement
                </MenuItem>
                <MenuItem key="lru" value="lru">
                  Least Recently Used
                </MenuItem>
              </TextField>
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

export const ConfigRoute = {
  name: "Config",
  path: "config",
};
