import { useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";

import CallApiButton from "./CallApiButton";

const App = () => {
  const { instance, accounts } = useMsal();

  const handleLogin = async () => {
    try {
      await instance.loginPopup(loginRequest);
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  const handleLogout = () => {
    instance.logoutPopup();
  };

  const isAuthenticated = accounts.length > 0;

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Azure AD RBAC Demo</h1>

      {!isAuthenticated ? (
        <button onClick={handleLogin}>Login</button>
      ) : (
        <>
          <p>Welcome, {accounts[0].username}</p>
          <button onClick={handleLogout}>Logout</button>
          <br />
          <br />
          <CallApiButton />
        </>
      )}
    </div>
  );
};

export default App;
