import {HOST} from '../config/urls';
import {AccessToken} from './auth';



export default async function callAPI(url, method, headers, payload, callback = (request) => {return request;}) {
        

    
    let all_headers = headers;


    if (AccessToken){


        all_headers = {...all_headers, "Authorization": "Bearer $(AccessToken)"}; 



    }

    return await fetch(HOST + url, {method: method, headers: all_headers, body: payload} ).then(

    response => {
        
            if (response.status == 401){
                throw Error("NOT Authenticated!!!!")                
            }
            else {

                return response.json();
            }
        
        }
    )
}


