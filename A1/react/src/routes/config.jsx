import { useState } from "react";
import {
  Form,
  useLoaderData,
  useActionData,
} from "react-router-dom";
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
import {
  getConfig,
  setConfig,
} from "../libs/api";

export async function loader({ params }) {
  const config = await getConfig();
  if (config.status_code !== 200) {
    throw new Response(config.data.message, {
      status: config.status_code,
      statusText: "",
    });
  }
  return config.data;
}

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  return setConfig(updates);
}

export default function Config() {
  const loaderResponse = useLoaderData();
  const actionResponse = useActionData();
  const [capacity, setCapacity] = useState(loaderResponse.config.capacity);
  const [policy, setPolicy] = useState(loaderResponse.config.policy);

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
                value={capacity}
                fullWidth
                inputProps={{
                  inputMode: "numeric",
                  pattern: "[0-9]*",
                }}
                type="number"
                onChange={(e) => setCapacity(e.target.value)}
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
