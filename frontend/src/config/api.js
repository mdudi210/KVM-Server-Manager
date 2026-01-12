// API Configuration
// This file can be updated to change the API base URL
// For production, set this to use relative URLs or your server's IP

// Get API URL from environment variable or use default
const getApiUrl = () => {
  // Check if we're in development mode
  if (process.env.NODE_ENV === 'development') {
    return process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000';
  }
  
  // For production, use relative URLs (same origin as the frontend)
  // When served through nginx, this will automatically use the correct origin
  return window.location.origin;
};

export const API_BASE_URL = getApiUrl();

// Helper function to make API calls
export const apiCall = async (endpoint, options = {}) => {
  const url = endpoint.startsWith('http') 
    ? endpoint 
    : `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
  
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
};

export default {
  API_BASE_URL,
  apiCall,
};
