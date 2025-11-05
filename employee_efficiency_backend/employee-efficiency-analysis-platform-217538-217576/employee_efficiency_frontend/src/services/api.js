//
// PUBLIC_INTERFACE
// API service helper for Employee Efficiency Frontend
// Sets API_BASE_URL default to http://localhost:3001 and allows override via environment variables.
//
/** Get the API base URL for backend requests. */
export function getApiBaseUrl() {
  // Common patterns for Create React App and Vite
  const envUrl =
    process?.env?.REACT_APP_API_BASE_URL ||
    process?.env?.VITE_API_BASE_URL ||
    process?.env?.API_BASE_URL;

  const base = envUrl && envUrl.trim().length > 0 ? envUrl.trim() : "http://localhost:3001";
  // Strip trailing slash for consistency
  return base.endsWith("/") ? base.slice(0, -1) : base;
}

// PUBLIC_INTERFACE
/** Build a full URL from a path like "/upload" */
export function apiUrl(path) {
  /** Return the full API url for a relative path. */
  const root = getApiBaseUrl();
  if (!path) return root;
  return path.startsWith("/") ? `${root}${path}` : `${root}/${path}`;
}

// Example minimal fetch wrapper (can be extended in actual frontend code)
export async function apiGet(path, options = {}) {
  const res = await fetch(apiUrl(path), {
    method: "GET",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `GET ${path} failed with status ${res.status}`);
  }
  return res.json();
}
