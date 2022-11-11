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
  // return responseAdapter(data);
  console.log(`Pool updated in ${mode}: ${JSON.stringify(config)}`);
  return responseAdapter(
    mode === "automatic" ? {
      "success": "true",
      "content": "Pool updated",
    } : {
      "success": "true",
      "content": "Placeholder"
    }
  );
}

// Path: react/manager/src/routes/status.jsx
export async function getStatus() {
  const data = await request("/api/manager/aggregate_stats")
  // return responseAdapter(data);
  return responseAdapter({
    "success": "true",
    "content": {
      "miss_rate": [168, 1241, 327, 281, 565, 569, 307, 387, 267, 988, 320, 348, 335, 722, 238, 217, 331, 344, 590, 262, 382, 122, 430, 221, 415, 251, 873, 702, 371, 292],
      "hit_rate": [4168, 12441, 3297, 2801, 5465, 5609, 3907, 3487, 2967, 4988, 3620, 3648, 3635, 7262, 2138, 2177, 3431, 3424, 5990, 5262, 3882, 10322, 4370, 2621, 4715, 2951, 8873, 7002, 3711, 2692], 
      "number_of_items_in_cache": [4168, 12441, 3297, 2801, 5465, 5609, 3907, 3487, 2967, 4988, 3620, 3648, 3635, 7262, 2138, 2177, 3431, 3424, 5990, 5262, 3882, 10322, 4370, 2621, 4715, 2951, 8873, 7002, 3711, 2692],
      "total_size_of_items_in_cache": [4168, 12441, 3297, 2801, 5465, 5609, 3907, 3487, 2967, 4988, 3620, 3648, 3635, 7262, 2138, 2177, 3431, 3424, 5990, 5262, 3882, 10322, 4370, 2621, 4715, 2951, 8873, 7002, 3711, 2692],
      "number_of_requests_served_per_minute": [4168, 12441, 3297, 2801, 5465, 5609, 3907, 3487, 2967, 4988, 3620, 3648, 3635, 7262, 2138, 2177, 3431, 3424, 5990, 5262, 3882, 10322, 4370, 2621, 4715, 2951, 8873, 7002, 3711, 2692]
    }
  });
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
  // return responseAdapter(data);
  return responseAdapter(
    mode === "cache" ? {
      "success": "true",
      "content": [

      ]
    } : {
      "success": "true",
      "content": "All data are successfully deleted"
    }
  );
}

// Path: react/manager/src/routes/config.jsx
export async function getConfig(mode) {
  // mode =   "poolsize" | "cache"
  const data = await request(`/api/manager/${mode}/config`)
  // return responseAdapter(data);
  return responseAdapter(mode === "poolsize" ? {
    "success": "true",
    "content": {
      "resize_pool_option": "automatic",
      "resize_pool_parameters": {
        "max_miss_rate_threshold": 0,
        "min_miss_rate_threshold": 50,
        "ratio_expand_pool": 1,
        "ratio_shrink_pool": 1,
        "auto_mode": "true"
      }
    }
  } : {
    "success": "true",
    "content": {
      "capacity": 100,
      "replacement_policy": "rr"
    }
  }
  );
}

// Path: react/manager/src/routes/config.jsx
export async function getPoolSize() {
  const data = await request("/api/manager/poolsize")
  // return responseAdapter(data);
  return responseAdapter({
    "success": "true",
    "content": 1
  });
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
  // return responseAdapter(data);
  return responseAdapter({
    "success": "true",
    "content": "Cache config is successfully updated"
  });
}

function responseAdapter(response) {
  // const output = response;
  // output.success = output.success === "true";
  // return output;
  return {
    data: response,
    status: 200,
    statusText: "OK",
  }
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