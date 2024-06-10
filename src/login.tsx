import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import callAPI from './utils/callAPI';
import {setTokens} from './utils/auth';


export default function LoginPage() {

    return (
    <div className='LoginPage'>
        <LoginTile/>
        </div>
    );
}

function LoginTile() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    let navigate = useNavigate();

    function onSubmit(event) {
        callAPI("/users/token", "POST", {'Content-Type': 'application/json'},JSON.stringify({"username": username, "password": password})).then(response_data => {
            console.log(response_data)
        setTokens(response_data.access, response_data.refresh);})
    }




    return (
        <div className='LoginTile'>
			<div className='LoginForm'> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="username">Username</label>
					<input type="text" name="username" id="username" value = {username} onChange={(e) => {setUsername(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="password">Password</label>
					<input type="password" name="password" id="password" value={password} onChange={(e) => {setPassword(e.target.value)}}/> 
				</div>  
				<button className='LoginSubmitButton' onClick={onSubmit}>Login</button>
                <p>--or--</p>
                <a className='SignUpLink' onClick={()=>navigate('/signup')}>Sign Up</a>
			</div>
        </div>
    )
}
