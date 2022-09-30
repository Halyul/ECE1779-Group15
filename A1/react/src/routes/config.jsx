import { useState } from "react";
import { Form, useLoaderData, useActionData } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardActions,
  CardContent,
  MenuItem,
  Button,
  TextField,
  Grid,
} from "@mui/material";
import { getConfig, setConfig } from "../libs/api";
import SubmissionPrompt from "../components/submission-prompt";
import { TooltipOnError } from "../components/tooltip";

export async function loader({ params }) {
  const response = await getConfig();
  if (response.status !== 200) {
    throw new Response(config.data.message, {
      status: response.status,
      statusText: response.statusText,
    });
  }
  return response.data;
}

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  const response = await setConfig(updates);
  return {
    status: response.status,
    statusText: response.statusText,
  };
}

export default function Config() {
  const loaderResponse = useLoaderData();
  const actionResponse = useActionData();
  const [capacity, setCapacity] = useState(loaderResponse.config.capacity);
  const [policy, setPolicy] = useState(loaderResponse.config.policy);
  const [submitted, setSubmitted] = useState(false);
  const [capacityError, setCapacityError] = useState(false);

  return (
    <>
      <Card>
        <CardHeader title="Configuration" />
        <Form
          id="config-form"
          method="POST"
          onSubmit={(e) => {
            setSubmitted(true);
          }}
        >
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TooltipOnError
                  open={capacityError}
                  handleClose={() => setCapacityError(false)}
                  title="Please enter a positive integer."
                  body={
                    <TextField
                      id="config-form-capacity"
                      name="capacity"
                      label="Capacity in MB"
                      variant="outlined"
                      value={capacity}
                      fullWidth
                      onChange={(e) => {
                        try {
                          const value = parseInt(e.target.value);
                          setCapacity(value || "");
                          if (value >= 0) {
                            setCapacityError(false);
                          } else {
                            setCapacityError(true);
                          }
                        } catch {
                          setCapacity(0);
                          setCapacityError(true);
                        }
                      }}
                      error={capacityError}
                    />
                  }
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
                  required
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
            <Button
              size="small"
              type="submit"
              onClick={(e) => {
                if (capacity < 0) {
                  setCapacityError(true);
                  e.preventDefault();
                }
              }}
            >
              Submit
            </Button>
          </CardActions>
        </Form>
      </Card>
      <SubmissionPrompt
        failed={{
          title: "Failed to update configuration",
          text: actionResponse?.statusText,
        }}
        submitting={{
          text: "Configuration is updating...",
          open: submitted,
          setOpen: setSubmitted,
        }}
        submittedText="Configuration updated successfully"
        submissionStatus={actionResponse}
      />
    </>
  );
}

export const ConfigRoute = {
  name: "Config",
  path: "config",
};
