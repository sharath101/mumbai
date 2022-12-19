import './App.css';
import Login from './components/login';
import { useState, useEffect } from 'react';
import { getRequest } from './utils/axios';

function App() {
    const [logInfo, setLogInfo] = useState({
        googledIn: false,
        accessToken: '',
        loggedIn: false,
    });
    const [user, setUser] = useState({
        name: '',
        email: '',
        ign: '',
        steamId: '',
        pic: '',
    });

    const checkLogin = async () => {
        try {
            const response = await getRequest('/login');
            if (response.status === 200 && response.data.success) {
                setLogInfo({ ...setLogInfo, loggedIn: true, googledIn: true });
                setUser({
                    ign: response.data.data.ign,
                    steamId: response.data.data.steamId,
                    pic: response.data.data.picture,
                    email: response.data.data.email,
                    name: response.data.data.name,
                });
            }
        } catch (err) {
            console.log('Server error while logging in');
        }
    };

    useEffect(() => {
        checkLogin();
    }, []);

    return (
        <div>
            <header id='header' className='fixed-top  '>
                <div className='container-fluid d-flex align-items-center justify-content-lg-between'>
                    <div className='row col-md-12'>
                        <div className='col-md-2'>
                            <h1 className='logo me-auto me-lg-0 d-flex justify-content-center'>
                                <a href='index.html'>
                                    Gp<span>.</span>
                                </a>
                            </h1>
                        </div>
                        <div className='col-md-8'>
                            <nav
                                id='navbar'
                                className='navbar order-last order-lg-0 d-flex justify-content-center'
                            >
                                <ul>
                                    <li>
                                        <a
                                            className='nav-link scrollto active'
                                            href='#hero'
                                        >
                                            Home
                                        </a>
                                    </li>
                                    <li>
                                        <a
                                            className='nav-link scrollto'
                                            href='#about'
                                        >
                                            About
                                        </a>
                                    </li>
                                    <li>
                                        <a
                                            className='nav-link scrollto'
                                            href='#tournaments'
                                        >
                                            Tournaments
                                        </a>
                                    </li>
                                    <li>
                                        <a
                                            className='nav-link scrollto '
                                            href='#leaderboard'
                                        >
                                            Leaderboard
                                        </a>
                                    </li>
                                    <li>
                                        <a
                                            className='nav-link scrollto'
                                            href='#contact'
                                        >
                                            Contact
                                        </a>
                                    </li>
                                </ul>
                                <i className='bi bi-list mobile-nav-toggle'></i>
                            </nav>
                        </div>
                        <div className='col-md-2'>
                            <div className='d-flex justify-content-center'>
                                <Login
                                    logInfo={logInfo}
                                    setLogInfo={setLogInfo}
                                    user={user}
                                    setUser={setUser}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </header>
            <div className='container'></div>
        </div>
    );
}

{
    /* <Login
                logInfo={logInfo}
                setLogInfo={setLogInfo}
                user={user}
                setUser={setUser}
              /> */
}

export default App;
