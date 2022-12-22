import Login from './login';

const NavBar = ({ logInfo, setLogInfo, user, setUser }) => {
    return (
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
                            <a className='nav-link scrollto active' href='/'>
                                Home
                            </a>
                        </li>
                        <li>
                            <a className='nav-link scrollto' href='#about'>
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
                            <a className='nav-link scrollto' href='#contact'>
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
    );
};

export default NavBar;
