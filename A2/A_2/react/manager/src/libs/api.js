// Path: react/manager/src/routes/config.jsx
export async function setModeParam(mode, config) {
  const data = await request(
    `/api/manager/poolsize/${mode}`,
    {
      method: "POST",
      body: JSON.stringify(config),
      headers: {
        "Content-Type": "application/json",
      },
    },
  )
  console.log(`Pool updated in ${mode}: ${JSON.stringify(config)}`);
  return responseAdapter(data);
}

// Path: react/manager/src/routes/status.jsx
export async function getStatus() {
  const data = await request("/api/manager/aggregate_stats")
  return responseAdapter(data);
}

// Path: react/manager/src/routes/config.jsx
export async function clear(mode) {
  const data = await request(
    `/api/manager/${mode}/clear`,
    {
      method: "DELETE",
    },
  )
  console.log(`Cleared: ${mode}`);
  return responseAdapter(data);
}

// Path: react/manager/src/routes/config.jsx
export async function getConfig(mode) {
  // mode =   "poolsize" | "cache"
  const data = await request(`/api/manager/${mode}/config`)
  return responseAdapter(data);
}

// Path: react/manager/src/routes/config.jsx
export async function getPoolSize() {
  const data = await request("/api/manager/poolsize")
  return responseAdapter(data);
}

// Path: react/manager/src/routes/config.jsx
export async function setNodeConfig(config) {
  const data = await request(
    "/api/manager/cache/config",
    {
      method: "POST",
      body: JSON.stringify(config),
      headers: {
        "Content-Type": "application/json",
      },
    },
  )
  console.log(`Node updated: ${JSON.stringify(config)}`);
  return responseAdapter(data);
}

function responseAdapter(response) {
  const output = response;
  output.success = output.success === "true";
  return output;
}

async function request(
  url,
  options = {},
) {
  return fetch(url, options)
    .then((res) => {
      if (res.ok) {
        return res.json().then((data) => {
          return {
            data,
            status: res.status,
            statusText: res.statusText,
          };
        });
      }
      return Promise.reject(res)
    })
    .catch((error) => {
      console.error("Error:", error);
      if (error.message) {
        return {
          data: {
            success: false,
            message: error.message,
          },
          status: 500,
          statusText: error.message,
        }
      }
      if (typeof error === "object") {
        return {
          data: {
            success: false,
            message: error.statusText,
          },
          status: error.status,
          statusText: error.statusText,
        }
      }
      return error.json().then((data) => {
        return {
          data: {
            success: error.ok,
            message: data.error.message,
          },
          status: error.status,
          statusText: error.statusText,
        }
      })
    });
};