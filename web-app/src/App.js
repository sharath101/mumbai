import './App.css';
import { useState, useEffect } from 'react';
import { getRequest } from './utils/axios';
import { BrowserRouter } from 'react-router-dom';
import NavBar from './components/navBar';
import Routes from './routes/router';

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
        <div className='container-fluid'>
            <header id='header' className='navbar-custom'>
                <div className='container-fluid d-flex align-items-center justify-content-lg-between'>
                    <NavBar
                        user={user}
                        setUser={setUser}
                        logInfo={logInfo}
                        setLogInfo={setLogInfo}
                    />
                </div>
            </header>
            {/* <BrowserRouter>
                <Routes
                    user={user}
                    setUser={setUser}
                    logInfo={logInfo}
                    setLogInfo={setLogInfo}
                />
            </BrowserRouter> */}
        </div>
    );
}

export default App;
