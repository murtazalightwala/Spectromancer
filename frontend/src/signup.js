import React, {useState} from 'react';
import AuthService from './utils/services/auth';


export default function SignUpPage() {


    return (
        <div className='SignUpPage'>
            <SignUpTile/>
            </div>
        );
}

function SignUpTile() {

    const [first_name, setFirstName] = useState("");
    const [last_name, setLastName] = useState("");
    const [username, setUserName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [retype_password, setRePassword] = useState("");
    const [avatar_url, setAvatarUrl] = useState("");
    const [special, setSpecial] = useState("");
    const [mobile, setMobile] = useState("");
    const [errors, setErrors] = useState("");

    function onSubmit(event) {
        if (password === retype_password){
            let user = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                    "password": password,
                };
        let response = AuthService.register(user, avatar_url, mobile, special);   
        }
        else{
            setErrors("Passwords don't match!!!!!")
        }
    }

    return (

        <div className='SignUpTile'>
			<div className='SignUpForm'> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="first_name">First Name</label>
					<input type="text" name="first_name" id="first_name" value = {first_name} onChange={(e) => {setFirstName(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="last_name">Last name</label>
					<input type="text" name="last_name" id="last_name" value = {last_name} onChange={(e) => {setLastName(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="username">Username</label>
					<input type="text" name="username" id="username" value = {username} onChange={(e) => {setUserName(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="email">E-mail</label>
					<input type="text" name="email" id="email" value = {email} onChange={(e) => {setEmail(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="mobile">Mobile Number</label>
					<input type="text" name="mobile" id="mobile" value = {mobile} onChange={(e) => {setMobile(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="special">Special</label>
					<input type="text" name="special" id="special" value = {special} onChange={(e) => {setSpecial(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="avatar_url">Avatar Url</label>
					<input type="text" name="avatar_url" id="avatar_url" value = {avatar_url} onChange={(e) => {setAvatarUrl(e.target.value)}}/> 
				</div> 
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="password">Password</label>
					<input type="password" name="password" id="password" value={password} onChange={(e) => {setPassword(e.target.value)}}/> 
				</div>  
				<div className='inputRow'> 
					<label className='LoginFormLabel' htmlFor="password">Retype Password</label>
					<input type="password" name="password" id="password" value={retype_password} onChange={(e) => {setRePassword(e.target.value)}}/> 
				</div>  
				<button className='LoginSubmitButton' onClick={onSubmit}>Submit</button>
    			</div>
        </div>
    )


}