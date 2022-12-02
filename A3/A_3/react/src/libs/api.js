import request from "./request";

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

export async function retrieveImage(key, shareKey) {
  const data = await request(
    `/api/${key ? "key" : "public"}/${key || shareKey}`,
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