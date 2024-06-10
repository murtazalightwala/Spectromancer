import {HOST, AUTH_URLS} from '../config/urls';

export var AccessToken = null;
export var RefreshToken = null;



export default function refreshAuthToken() {
    
    response = fetch(HOST + AUTH_URLS.REFRESH_TOKEN, {method: "POST", body: {"refresh": RefreshToken}}).then(response => {
       if (response.ok) {

            data = response.json();
            console.log(data);
            AccessToken = data.access;
        
            return ;
        } 
    
        else {

         throw Error("Something went wrong while refreshing token!!!!!!");
        }
    })
}


export function setTokens(access_token, refresh_token) {
    AccessToken = access_token;
    RefreshToken = refresh_token;
    console.log(AccessToken);

}
