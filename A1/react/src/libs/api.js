export async function upload(requestData) {
  const formData = new FormData();
  for(const name in requestData) {
    formData.append(name, requestData[name]);
  }
  const data = await request(
    "/api/upload",
    {
      method: "POST",
      body: formData,
      headers: {},
    }
  )
  return responseAdapter(data);
}

export async function retrieveKeys() {
  /*
    {
      "success": "true",
      "keys": [Array of keys(strings)]
    }
  */
  const data = await request(
    "/api/list_keys",
    {
      method: "POST",
    }
  )
  return responseAdapter(data);
}

export async function retrieveImage(key) {
  /*
    {
      "success": "true", // string????
      “content” : file contents
    }
   */
  const data = await request(
    `/api/key/${key}`,
    {
      method: "POST",
    },
  )
  return responseAdapter(data);
}

export async function getConfig() {
  // return {
  //   success: true,
  //   config: {
  //     capacity: 10,
  //     policy: "lru",
  //   }
  // };
  const data = await request("/api/config")
  return responseAdapter(data);
}

export async function setConfig(config) {
  // return {
  //     success: true,
  //     config: {
  //       capacity: 20,
  //       policy: "rr",
  //     }
  //   }
  const data = await request(
    "/api/config",
    {
      method: "POST",
      body: JSON.stringify(config),
    },
  )
  return responseAdapter(data);
}

export async function getStatus() {
  const data = await request("/api/status")
  return responseAdapter(data);
}

function responseAdapter(response) {
  const output = response;
  output.success = output.success === "true";
  return output;
}

async function request(
  url = "",
  {
    body,
    headers,
    method,
    ...options
  } = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    },
) {
  return fetch(url, {
    method,
    headers,
    body,
  })
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
      return error.text().then((text) => {
        return {
          data: {
            success: error.ok,
            message: text,
          },
          status: error.status,
          statusText: error.statusText,
        }
      })
    });
}