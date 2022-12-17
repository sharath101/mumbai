import './App.css';
import Login from './components/login'
import { useState } from 'react';
import { getRequest } from './utils/axios';

function App() {
  const [logInfo, setLogInfo] = useState({
      googledIn: false,
      accessToken: '',
      loggedIn: false
  })
  const [user, setUser] = useState({
    name: '',
    email: '',
    ign: '',
    steamId: '',
    pic: '',
  })

  const checkLogin = async () => {
    try {
      console.log('enter');
      const response = await getRequest('/login');
      console.log(response);
      if(response.status === 200 && response.data.success) {
        setLogInfo({...setLogInfo, loggedIn: true, googledIn: true})
        setUser({
          ign: response.data.data.ign, 
          steamId: response.data.data.steamId, 
          pic: response.data.data.picture, 
          email: response.data.data.email,
          name:  response.data.data.name,
        })
      }
    } catch(err) {
      console.log('Error while checking login');
    }
  } 

  checkLogin();

  return (
    <header id="header" className="fixed-top ">
    <div className="container-fluid d-flex align-items-center justify-content-lg-between">
        <div class="row col-md-12">
            <div class="col-md-4 align-center">
              <h1 className="logo me-auto me-lg-0"><a href="index.html">Gp<span>.</span></a></h1>
            </div>
            <div className='col-md-6'>
              <nav id="navbar" className="navbar order-last order-lg-0">
                <ul>
                  <li><a class="nav-link scrollto active" href="#hero">Home</a></li>
                  <li><a class="nav-link scrollto" href="#about">About</a></li>
                  <li><a class="nav-link scrollto" href="#tournaments">Tournaments</a></li>
                  <li><a class="nav-link scrollto " href="#leaderboard">Leaderboard</a></li>
                  <li><a class="nav-link scrollto" href="#contact">Contact</a></li>
                </ul>
                <i className="bi bi-list mobile-nav-toggle"></i>
              </nav>
            </div>
            <div class="col-md-2">
              <Login
                logInfo={logInfo}
                setLogInfo={setLogInfo}
                user={user}
                setUser={setUser}
              />
            </div>
        </div>
    </div>
  </header>
  );
}

export default App;
