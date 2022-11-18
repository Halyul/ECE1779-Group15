import {
  useState,
  useEffect,
} from "react";
import {
  useActionData,
  useLoaderData
} from "react-router-dom";
import {
  MenuItem,
  Button,
  TextField,
  Grid,
  Slider,
  Typography,
} from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import {
  getConfig,
  getPoolSize,
  setNodeConfig,
  setModeParam,
  clear
} from "../libs/api";
import { ConfigCard } from "../components/card";
import SubmissionPrompt from "../components/submission-prompt";
import { TooltipOnError } from "../components/tooltip";

export async function loader({ params }) {
  const nodeConfig = await getConfig("cache");
  const poolConfig = await getConfig("poolsize");
  const poolSize = await getPoolSize();
  if (![nodeConfig.status === 200, poolConfig.status === 200, poolSize.status === 200].every((e) => e)) {
    throw new Response("Failed to retrieve configurations.", {
      status: 500,
      statusText: "Internal Server Error",
    });
  }
  const response = {
    node: nodeConfig.data.content,
    pool: {
      config: poolConfig.data.content,
      size: poolSize.data.content.size,
    },

  };
  return response;
}

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  console.log(updates)
  let response;
  switch (updates.clear) {
    case "true": {
      response = await clear(updates.api_method === "pool" ? "data" : "cache");
      break
    }
    default: {
      switch (updates.api_method) {
        case "node": {
          response = await setNodeConfig({
            capacity: updates.capacity,
            policy: updates.policy,
          });
          break
        }
        case "pool": {
          response = await setModeParam(updates.mode, {
            change: updates.change,
            max_miss_rate_threshold: updates.max_miss_rate_threshold,
            min_miss_rate_threshold: updates.min_miss_rate_threshold,
            expand_ratio: updates.expand_ratio,
            shrink_ratio: updates.shrink_ratio,
          });
          break
        }
      }
    }
  }
  return {
    status: response.status,
    statusText: response.data?.message || response.statusText,
  };
}

export default function Config() {
  const loaderResponse = useLoaderData();
  const actionResponse = useActionData();
  const [submitted, setSubmitted] = useState(false);

  const [capacity, setCapacity] = useState(loaderResponse.node.capacity);
  const [capacityError, setCapacityError] = useState(false);
  const [policy, setPolicy] = useState(loaderResponse.node.policy);
  const [clearCache, setClearCache] = useState(false);

  const [poolSize, setPoolSize] = useState(loaderResponse.pool.size);
  const [resizingMode, setResizingMode] = useState(loaderResponse.pool.config.resize_pool_option);
  const [missRateThreshold, setMissRateThreshold] = useState([loaderResponse.pool.config.resize_pool_parameters.min_miss_rate_threshold * 100 || 30, loaderResponse.pool.config.resize_pool_parameters.max_miss_rate_threshold * 100 || 80]);
  const [expandRatio, setExpandRatio] = useState(loaderResponse.pool.config.resize_pool_parameters.ratio_expand_pool || 1);
  const [expandRatioError, setExpandRatioError] = useState(false);
  const [shrinkRatio, setShrinkRatio] = useState(loaderResponse.pool.config.resize_pool_parameters.ratio_shrink_pool || 0.5);
  const [shrinkRatioError, setShrinkRatioError] = useState(false);
  const [manualNodeChange, setManualNodeChange] = useState("");
  const [clearData, setClearData] = useState(false);

  useEffect(() => {
    let timer
    const loop = () => {
      const fetchData = async () => {
        return await getPoolSize();
      }
      fetchData().then((response) => {
        if (response.status === 200) {
          setPoolSize(response.data.content.size);
          timer = setTimeout(loop, 1000)
        }
      });
    }
    loop()
    return () => clearTimeout(timer)
 }, [])

  return (
    <>
      <ConfigCard
        title="Configuration for memcache nodes"
        id="config-nodes-form"
        method="POST"
        onSubmit={(e) => {
          setSubmitted(true);
          setClearCache(false)
        }}
        content={
          <Grid container spacing={2}>
            <TextField
              hidden
              name="api_method"
              value="node"
            />
            <TextField
              hidden
              name="clear"
              value={clearCache}
            />
            <Grid item xs={12} sm={6}>
              <TooltipOnError
                open={capacityError}
                handleClose={() => setCapacityError(false)}
                title="Range: 0-2048 MB"
                body={
                  <TextField
                    id="config-node-capacity"
                    name="capacity"
                    label="Capacity in MB"
                    variant="outlined"
                    value={capacity}
                    fullWidth
                    onChange={(e) => {
                      try {
                        const value = parseInt(e.target.value);
                        setCapacity(value < 0 ? "" : (
                          isNaN(value) ? "" : value
                        ));
                        if (value >= 0 && value <= 2048) {
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
            <Grid item xs={12} sm={6}>
              <TextField
                id="config-node-policy"
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
        }
        actions={
          <>
            <Button
              size="small"
              type="submit"
              disabled={capacityError}
              onClick={(e) => {
                if (capacity < 0 || capacity > 2048 || capacity === "") {
                  setCapacityError(true);
                  e.preventDefault();
                }
              }}
            >
              Submit
            </Button>
            <Button
              size="small"
              color="error"
              type="submit"
              onClick={(e) => {
                setClearCache(true)
              }}
              sx={{ marginLeft: "auto" }}
            >
              Delete Cache
            </Button>
          </>
        }
      />
      <ConfigCard
        title="Configuration for the memcache pool"
        subtitle={`Current Pool Size: ${poolSize}`}
        id="config-pool-form"
        method="POST"
        onSubmit={(e) => {
          setSubmitted(true)
          setClearData(false)
          setManualNodeChange("")
        }}
        content={
          <>
            <TextField
              hidden
              name="api_method"
              value="pool"
            />
            <TextField
              hidden
              name="clear"
              value={clearData}
            />
            <TextField
              hidden
              name="change"
              value={manualNodeChange}
            />
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  id="config-pool-mode"
                  name="mode"
                  label="Resizing Mode"
                  variant="outlined"
                  value={resizingMode}
                  fullWidth
                  select
                  onChange={(event) => {
                    setResizingMode(event.target.value);
                  }}
                >
                  <MenuItem key="automatic" value="automatic">
                    Automatic
                  </MenuItem>
                  <MenuItem key="manual" value="manual">
                    Manual
                  </MenuItem>
                </TextField>
              </Grid>
              {
                resizingMode === "automatic" ? (
                  <>
                    <Grid item xs={12} sm={6}>
                      <TooltipOnError
                        open={expandRatioError}
                        handleClose={() => setExpandRatioError(false)}
                        title="Range: 1.0-∞"
                        body={
                          <TextField
                            id="config-pool-expand-ratio"
                            name="expand_ratio"
                            label="Expand Ration"
                            variant="outlined"
                            value={expandRatio}
                            fullWidth
                            onChange={(e) => {
                              const value = parseFloat(e.target.value).toFixed(2);
                              if (isNaN(value) || value < 1) {
                                setExpandRatioError(true);
                                setExpandRatio("");
                              } else {
                                setExpandRatio(e.target.value);
                                setExpandRatioError(false);
                              }
                            }}
                            error={expandRatioError}
                          />
                        }
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TooltipOnError
                        open={shrinkRatioError}
                        handleClose={() => setShrinkRatioError(false)}
                        title="Rnage: 0.0-1.0"
                        body={
                          <TextField
                            id="config-pool-shrink-ratio"
                            name="shrink_ratio"
                            label="Shrink Ration"
                            variant="outlined"
                            value={shrinkRatio}
                            fullWidth
                            onChange={(e) => {
                              const value = parseFloat(e.target.value);
                              if (isNaN(value) || value > 1 || value < 0) {
                                setShrinkRatioError(true);
                                setShrinkRatio("");
                              } else {
                                setShrinkRatio(e.target.value);
                                setShrinkRatioError(false);
                              }
                            }}
                            error={shrinkRatioError}
                          />
                        }
                      />
                    </Grid>
                    <Grid item xs={12} sx={{ margin: "0 1rem" }}>
                      <Typography
                        gutterBottom
                        variant="caption"
                      >
                        Miss Rate Threshold (%)
                      </Typography>
                      <TextField
                        hidden
                        name="min_miss_rate_threshold"
                        value={(parseFloat(missRateThreshold[0]) * 0.01).toFixed(2)}
                      />
                      <TextField
                        hidden
                        name="max_miss_rate_threshold"
                        value={(parseFloat(missRateThreshold[1]) * 0.01).toFixed(2)}
                      />
                      <Slider
                        getAriaLabel={() => 'Miss Rate Threshold'}
                        defaultValue={missRateThreshold}
                        onChange={(_, newValue, __) => setMissRateThreshold(newValue)}
                        valueLabelDisplay="auto"
                        getAriaValueText={(value) => `${value}%`}
                        disableSwap
                      />
                    </Grid>
                  </>
                ) : (
                  <>
                    <Grid item xs={12} sm={6}>
                      <Button
                        variant="outlined"
                        startIcon={<AddIcon />}
                        fullWidth
                        type="submit"
                        onClick={(e) => {
                          setManualNodeChange("increase")
                        }}
                      >
                        Add One Node
                      </Button>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Button
                        variant="outlined"
                        endIcon={<RemoveIcon />}
                        fullWidth
                        type="submit"
                        onClick={(e) => {
                          setManualNodeChange("decrease")
                        }}
                      >
                        Remove One Node
                      </Button>
                    </Grid>
                  </>
                )
              }
            </Grid>
          </>
        }
        actions={
          <>
            <Button
              size="small"
              type="submit"
              disabled={resizingMode !== "automatic" || (expandRatioError || shrinkRatioError)}
              onClick={(e) => {
                const expandRatioValue = parseFloat(expandRatio).toFixed(2);
                const shrinkRatioValue = parseFloat(shrinkRatio).toFixed(2);
                if (isNaN(expandRatioValue) || expandRatioValue <= 1 || expandRatio === "") {
                  setExpandRatioError(true)
                  e.preventDefault()
                  return
                }
                if (isNaN(shrinkRatioValue) || shrinkRatioValue >= 1 || shrinkRatioValue <= 0 || shrinkRatio === "") {
                  setShrinkRatioError(true)
                  e.preventDefault()
                  return
                }
                setExpandRatio(expandRatioValue)
                setShrinkRatio(shrinkRatioValue)
              }}
            >
              Submit
            </Button>
            <Button
              size="small"
              color="error"
              type="submit"
              onClick={(e) => {
                setClearData(true)
              }}
              sx={{ marginLeft: "auto" }}
            >
              Delete All Data
            </Button>
          </>
        }
      />
      <SubmissionPrompt
        failed={{
          title: "Failed to commit changes",
          text: actionResponse?.statusText,
        }}
        submitting={{
          text: "Commiting changes...",
          open: submitted,
          setOpen: setSubmitted,
        }}
        submittedText="Changes committed successfully"
        submissionStatus={actionResponse}
      />
    </>
  );
}

export const ConfigRoute = {
  name: "Config",
  path: "config",
};
