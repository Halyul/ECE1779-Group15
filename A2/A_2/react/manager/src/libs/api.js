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
  // return responseAdapter(data);
  console.log(`Pool updated in ${mode}: ${JSON.stringify(config)}`);
  return {
    status: 200,
    statusText: "OK",
  };
}

export async function getStatus(mode) {
  const data = await request(`/api/manager/${mode}`)
  return responseAdapter(data);
}

export async function clear(mode) {
  const data = await request(
    `/api/manager/${mode}/clear`,
    {
      method: "DELETE",
    },
  )
  // return responseAdapter(data);
  console.log(`Cleared: ${mode}`);
  return {
    status: 200,
    statusText: "OK",
  };
}

export async function getPoolConfig() {
  const data = await request("/api/manager/config")
  return responseAdapter(data);
}

export async function getNodeConfig() {
  const data = await request("/api/manager/config")
  return responseAdapter(data);
}

export async function setNodeConfig(config) {
  const data = await request(
    "/api/manager/config",
    {
      method: "POST",
      body: JSON.stringify(config),
      headers: {
        "Content-Type": "application/json",
      },
    },
  )
  // return responseAdapter(data);
  console.log(`Node updated: ${JSON.stringify(config)}`);
  return {
    status: 200,
    statusText: "OK",
  };
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