import { useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";
import { useState } from "react";

const CallApiButton = () => {
    const { instance, accounts } = useMsal();

    const [userResponse, setUserResponse] = useState("none");
    const [piiResponse, setPiiResponse] = useState("none");
    const [adminResponse, setAdminResponse] = useState("none");



    const callApi = async (endpoint: string) => {
        try {
            const response = await instance.acquireTokenSilent({
                ...loginRequest,
                account: accounts[0],
            });

            const token = response.accessToken;

            const apiResponse = await fetch("http://localhost:8000/" + endpoint, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const data = await apiResponse.json();
            console.log("API Response:", data);
            return data;
        } catch (error) {
            console.error("API call failed:", error);
        }
    };

    const callAdmin = async () => {
        const res = await callApi('admin');
        setAdminResponse(JSON.stringify(res));
    }

    const callPii = async () => {
        const res = await callApi('pii');
        setPiiResponse(JSON.stringify(res));
    }

    const callUser = async () => {
        const res = await callApi('user');
        setUserResponse(JSON.stringify(res));
    }

    return (
        <>

            <button onClick={callUser}>Call User</button>
            {userResponse}

            <button onClick={callPii}>Call PII</button>
            {piiResponse}
            <button onClick={callAdmin}>Call Admin Api </button>
            {adminResponse}


        </>
    );
};

export default CallApiButton;
