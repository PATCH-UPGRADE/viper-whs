const CARTHAGE_API_URL = import.meta.env.VITE_CARTHAGE_API_URL;

if (!CARTHAGE_API_URL) {
  throw new Error("'VITE_CARTHAGE_API_URL' not found in .env!");
}

export const carthageFetcher = async <T>(
  endpointUrl: string,
  options?: RequestInit,
): Promise<T> => {
  const response = await fetch(`http://${CARTHAGE_API_URL}${endpointUrl}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`An HTTP error occured: ${response.status}`);
  }

  return response.json();
};

// explicitly leave off the content-type so the browser can determine it
export const carthageFetcherUpload = async <T>(
  endpointUrl: string,
  options?: RequestInit,
): Promise<T> => {
  const response = await fetch(`http://${CARTHAGE_API_URL}${endpointUrl}`, {
    headers: {
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`An HTTP error occured: ${response.status}`);
  }

  return response.json();
};
