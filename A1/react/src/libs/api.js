import useSWR from "swr";

const fetcher = (url) => fetch(url).then((res) => res.json());

export function useTest() {
    const { data, error } = useSWR(
      "https://gorest.co.in/public/v2/users",
      fetcher
    );
  
    return {
        data: data,
        isLoading: !error && !data,
        isError: error
    }
  }