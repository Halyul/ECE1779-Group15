export async function upload(requestData) {
  const data = await request(
    "/api/upload",
    "POST",
    requestData,
    {
      "Content-Type": "multipart/form-data",
    },
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
      "POST"
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
      "POST",
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
  const data = await request(
    "/api/config",
    "GET",
  )
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
    "POST",
    JSON.stringify(config),
  )
  return responseAdapter(data);
}

export async function getStatus() {
  const data = await request(
    "/api/status",
    "GET",
  )
  return responseAdapter(data);
}

function responseAdapter(response) {
  const output = response;
  output.success = output.success === "true";
  return output;
}

async function request(
  url = "",
  method = "GET",
  body = null, // body data type must match "Content-Type" header
  headers = {
    "Content-Type": "application/json",
  },
) {
  try {
    const response = await fetch(url, {
      method: method,
      headers: headers,
      referrerPolicy: "no-referrer",
      body: body
    })
    const data = await response.json()
    const status_code = response.status
      return {
        data,
        status_code
      }
  } catch (e) {
    return {
      data: {
        success: false,
        message: e.message,
      },
      status_code: 400
    }
  }
}