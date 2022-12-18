export async function upload(requestData) {
  const formData = new FormData();
  for (const name in requestData) {
    formData.append(name, requestData[name]);
  }
  const user = get_user();
  formData.append("user", user.username);
  formData.append("role", user.role);
  const data = await request(
    "/api/upload",
    {
      method: "POST"
    },
    formData
  )
  return responseAdapter(data);
}

export async function retrieveKeys(admin = false) {
  const data = await request(
    "/api/photos",
    {
      method: "POST",
      body: { admin }
    }
  )
  const adapter = (input) => {
    return {
      ...input,
      data: {
        ...input.data,
        images: input.data.images?.map((image) => {
          return {
            ...image,
            share_link: image.is_shared === "False" ? null : image.share_link
          }
        })
      }
    }
  }
  return adapter(responseAdapter(data));
}

export async function retrieveImage(key, share_key) {
  key = key || share_key;
  const data = await request(
    `/api/key`,
    {
      method: "POST",
      body: share_key ? {
        key,
        user: null,
        role: null,
      } : { key }
    }
  )
  const adapter = (input) => {
    return {
      ...input,
      data: {
        ...input.data,
        image: [
          {
            ...input.data.image[0],
            share_link: input.data.image[0].is_shared === "False" ? null : input.data.image[0].share_link
          }
        ]
      }
    }
  }
  return adapter(responseAdapter(data));
}

export async function deleteImage(key) {
  const data = await request(
    `/api/key`,
    {
      method: "DELETE",
      body: { key }
    }
  )
  return responseAdapter(data); 
}

export async function share(key, is_shared = false) {
  const data = await request(
    `/api/share`,
    {
      method: "POST",
      body: {
        key,
        is_shared: is_shared ? "True" : "False"
      }
    }
  )
  const adapter = (input) => {
    return {
      ...input,
      data: {
        ...input.data,
        image: [
          {
            ...input.data.image,
            share_link: input.data.image.is_shared === "False" ? null : input.data.image.share_link
          }
        ]
      }
    }
  }
  return adapter(responseAdapter(data));
}

export async function getStats() {
  const data = await request(
    `/api/stats`,
    {
      method: "POST",
    }
  ) 
  return responseAdapter(data);
}

function responseAdapter(response) {
  const output = response;
  output.success = output.success === "true";
  return output;
}

function get_user() {
  return JSON.parse(JSON.parse(window.localStorage.getItem("persist:root")).user);
}

export default async function request(
  url,
  options = {},
  body = null,
) {
  const user = get_user()
  if (!body) options.headers = { "Content-Type": "application/json" }
  return fetch(import.meta.env.VITE_BACKEND_URL + url, {
    ...options,
    headers: {
      ...options.headers,
      "X-Access-Token": user.accessToken,
      "X-Id-Token": user.idToken,
    },
    body: body ? body : JSON.stringify({

      "user": user.username,
      "role": user.role,
      ...options.body,
    }),
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