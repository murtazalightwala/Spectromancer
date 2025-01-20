import {HOST, AUTH_URLS} from '../config/urls';
import {useState} from 'react';

export const [AccessToken, setAccessToken] = useState("NA");
export const [RefreshToken, setRefreshToken] = useState("NA");

export default function refreshAuthToken() {
    
    response = fetch(HOST + AUTH_URLS.REFRESH_TOKEN, {method: "POST", body: {"refresh": RefreshToken}}).then(response => {
       if (response.ok) {

            data = response.json();
            console.log(data);
            setAccessToken(data.acces);
        
            return ;
        } 
    
        else {

         throw Error("Something went wrong while refreshing token!!!!!!");
        }
    })
}


export function setTokens(access_token, refresh_token) {
     setAccessToken(access_token);
    setRefreshToken(refresh_token);
    console.log(AccessToken);

};

