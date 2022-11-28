export default async function request(
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