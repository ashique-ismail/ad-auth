// src/authConfig.js
export const msalConfig = {
  auth: {
    clientId: "ec24affa-6a8b-4ce4-85e1-d9b47301f537",
    authority: "https://login.microsoftonline.com/c71f69f4-ad2b-47c5-9bb1-f5b3317cdf3d",
    redirectUri: "http://localhost:5173",
  },
  cache: {
    cacheLocation: "localStorage",
  },
};

export const loginRequest = {
  scopes: ["api://sp-poc-fast_api-copilot/.default"],
};
