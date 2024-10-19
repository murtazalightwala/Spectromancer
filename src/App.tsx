import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import './App.css';
import LoginPage from './login';
import background from './landing_background.png';
import SignUpPage from "./signup";
import HomePage from './home';



function App() {
  return (
    <div className="App" style={{backgroundImage:`url(${background})`, height:"100vh", width:"100vw", justifySelf: "stretch"}}>
      <NavBar/>
      <BrowserRouter>
      <Routes>
      <Route path='/login' element={<LoginPage />}/>
      <Route path='/' element={<LoginPage />}/>
      <Route path='/signup' element={<SignUpPage />}/>
        <Route path='/home' element={<HomePage />}/>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

function NavBar() {

  return (
    <div className='NavBar'>
<ul>
  <li>Home</li>
  <li>Game</li>
  <li>Cards</li>
</ul>
    </div>
  )

}



export default App;
