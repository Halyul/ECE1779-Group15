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

export async function retrieveKeys(admin = false) {
  const data = await request(
    "/api/photos",
    {
      method: "POST",
      body: JSON.stringify({ admin })
    }
  )
  // return responseAdapter(data);
  return {
    status: 200,
    data: {
      images: [
        {
          key: "ajksdfghbuiagda", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
          tag: "test",
          is_shared: true,
        },
        {
          key: "gura", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/0.jpg",
          tag: "nan",
          is_shared: false,
        },
        {
          key: "78", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/404.jpg",
          tag: "nan",
          is_shared: true,
        },
        {
          key: "8", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/200.jpg",
          tag: "nan",
          is_shared: false,
        },
        {
          key: "12381", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/302.jpg",
          tag: "nan",
          is_shared: true,
        },
        {
          key: Math.random().toString(), // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/414.jpg",
          tag: "nan",
          is_shared: false,
        }
      ]
    }
  }
}

export async function retrieveImage(key, shareKey) {
  const data = await request(
    `/api/${key ? "key" : "public"}/${key || shareKey}`,
    {
      method: "POST",
    }
  )
  // return responseAdapter(data);
  return [
    {
      status: 200,
      data: {
        image: {
          content: "https://gura.ch/images/0.jpg",
          key: "gura",
          tag: "nan",
          share_link: "123",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
        }
      }
    },
    {
      status: 200,
      data: {
        image: {
          content: "https://gura.ch/images/404.jpg",
          key: "gura",
          tag: "test",
          share_link: null,
          number_of_access: -1,
          last_time_accessed: "27/11/2022 19:19:36",
        }
      }
    }
  ][Math.floor(Math.random() * 2)]
}

export async function deleteImage(key, admin = false) {
  const data = await request(
    `/api/key/${key}`,
    {
      method: "DELETE",
      body: JSON.stringify({ admin })
    }
  )
  // return responseAdapter(data);
  return {
    status: 200
  }
}

export async function createShare(key) {
  const data = await request(
    `/api/share`,
    {
      method: "POST",
      body: JSON.stringify({ key })
    }
  )
  // return responseAdapter(data);
  return {
    status: 200,
    data: {
      image: {
        content: "https://gura.ch/images/404.jpg",
        key: "gura",
        tag: "test",
        share_link: "456",
        number_of_access: 0,
        last_time_accessed: "27/11/2022 19:19:36",
      }
    }
  }
}

export async function deleteShare(key, admin = false) {
  const data = await request(
    `/api/share`,
    {
      method: "DELETE",
      body: JSON.stringify({ key, admin })
    }
  )
  // return responseAdapter(data);
  return {
    status: 200,
    data: {
      image: {
        content: "https://gura.ch/images/0.jpg",
        key: "gura",
        tag: "nan",
        share_link: null,
        number_of_access: -1,
        last_time_accessed: "27/11/2022 19:19:36",
      }
    }
  }
}

export async function getStats() {
  const data = await request(
    `/api/stats`,
    {
      method: "GET",
    }
  )
  // return responseAdapter(data);
  return {
    status: 200,
    data: {
      stats: [
        { name: 'Jon', value: true },
        { name: 'Cersei', value: 42 },
        { name: 'Jaime', value: 45 },
        { name: 'Arya', value: 16 },
        { name: 'Daenerys', value: null },
        { name: "lol", value: 150 },
        { name: 'Ferrara', value: 44 },
        { name: 'Rossini', value: 36 },
        { name: 'Harvey', value: 65 },
      ]
    }
  }
}

function responseAdapter(response) {
  const output = response;
  output.success = output.success === "true";
  return output;
}

export default async function request(
  url,
  options = {}
) {
  const user = JSON.parse(JSON.parse(window.localStorage.getItem("persist:root")).user);
  return fetch(url, {
    headers: {
      "X-Access-Token": user.accessToken,
      "X-Id-Token": user.idToken,
      "X-Username": user.username,
      "X-Role": user.role,
      ...options.headers,
    },
    ...options,
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