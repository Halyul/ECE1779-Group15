export async function upload(requestData) {
  const formData = new FormData();
  for (const name in requestData) {
    formData.append(name, requestData[name]);
  }
  const data = await request(
    "/api/upload",
    {
      method: "POST",
      body: formData
    }
  )
  return responseAdapter(data);
}

export async function retrieveKeys() {
  const data = await request(
    "/api/list_keys",
    {
      method: "POST",
    }
  )
  // return responseAdapter(data);
  return {
    data: {
      keys: []
    },
    status: 200,
    statusText: "OK",
  }
}

export async function retrieveImage(key) {
  const data = await request(
    `/api/key/${key}`,
    {
      method: "POST",
    },
  )
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
      // CASE: Network error
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
      // CASE: HTTP error
      return error.headers.get('content-type')?.includes('application/json') ? error.json().then((data) => {
        return {
          data: {
            success: error.ok,
            message: data.error.message,
          },
          status: error.status,
          statusText: error.statusText,
        }
      }) : error.text().then((data) => {
        return {
          data: {
            success: error.ok,
            message: data,
          },
          status: error.status,
          statusText: error.statusText,
        }
      })
    });
};