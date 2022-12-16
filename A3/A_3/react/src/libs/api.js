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
      body: { admin }
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
          share_link: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
        },
        {
          key: "gura", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/0.jpg",
          tag: "nan",
          share_link: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
        },
        {
          key: "78", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/404.jpg",
          tag: "nan",
          share_link: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
        },
        {
          key: "8", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/200.jpg",
          tag: "nan",
          share_link: null,
        },
        {
          key: "12381", // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/302.jpg",
          tag: "nan",
          share_link: "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
        },
        {
          key: Math.random().toString(), // the image key
          user: "gura",
          number_of_access: 1,
          last_time_accessed: "27/11/2022 19:19:36",
          thumbnail: "https://gura.ch/images/414.jpg",
          tag: "nan",
          share_link: null,
        }
      ]
    }
  }
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
  // return responseAdapter(data);
  return [
    {
      status: 200,
      data: {
        image: {
          content: "https://gura.ch/images/0.jpg",
          key: key,
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
          key: key,
          tag: "test",
          share_link: null,
          number_of_access: -1,
          last_time_accessed: "27/11/2022 19:19:36",
        }
      }
    }
  ][Math.floor(Math.random() * 2)]
}

export async function deleteImage(key) {
  const data = await request(
    `/api/key`,
    {
      method: "DELETE",
      body: { key }
    }
  )
  // return responseAdapter(data);
  return {
    status: 200
  }
}

export async function share(key, is_shared = false) {
  const data = await request(
    `/api/share`,
    {
      method: "POST",
      body: {
        key,
        is_shared
      }
    }
  )
  // return responseAdapter(data);
  return is_shared ? ({
    status: 200,
    data: {
      image: {
        content: "https://gura.ch/images/404.jpg",
        thumbnail: "https://gura.ch/images/404.jpg",
        user: "gura",
        key: key,
        tag: "test",
        share_link: "456",
        number_of_access: 0,
        last_time_accessed: "27/11/2022 19:19:36",
      }
    }
  }) : ({
    status: 200,
    data: {
      image: {
        content: "https://gura.ch/images/0.jpg",
        thumbnail: "https://gura.ch/images/0.jpg",
        key: key,
        user: "gura",
        tag: "nan",
        share_link: null,
        number_of_access: -1,
        last_time_accessed: "27/11/2022 19:19:36",
      }
    }
  })
}

export async function getStats() {
  const data = await request(
    `/api/stats`,
    {
      method: "POST",
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
    ...options,
    headers: {
      ...options.headers,
      "X-Access-Token": user.accessToken,
      "X-Id-Token": user.idToken,
    },
    body: JSON.stringify({
      
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