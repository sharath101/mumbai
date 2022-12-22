import { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import Modal from './modal';
import Dropdown from 'react-bootstrap/Dropdown';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { postRequest } from '../utils/axios';
// import MenuItem from 'react-bootstrap/MenuItem';

const Login = ({ logInfo, setLogInfo, user, setUser }) => {
    const [error, setError] = useState('');

    const login = useGoogleLogin({
        onSuccess: async (tokenResponse) => {
            const body = {
                accessToken: tokenResponse.access_token,
            };
            try {
                const response = await postRequest('/login', body);
                console.log('First request response:');
                console.log(response);
                if (response.status === 200 && response.data.success) {
                    setUser({
                        ...user,
                        ign: response.data.data.ign,
                        steamId: response.data.data.steamId,
                        pic: response.data.data.picture,
                        email: response.data.data.email,
                        name: response.data.data.name,
                    });
                    setLogInfo({
                        ...logInfo,
                        loggedIn: true,
                        googledIn: true,
                        token: tokenResponse.access_token,
                    });
                    console.log(`Logged into app`);
                } else {
                    setLogInfo({
                        ...logInfo,
                        googledIn: true,
                        token: tokenResponse.access_token,
                    });
                    console.log(`Logged in with google alone`);
                }
                setError('');
            } catch (err) {
                console.log(
                    `Error logging with google: ${JSON.stringify(err)}`
                );
                setLogInfo({
                    ...logInfo,
                    googleIn: false,
                    token: tokenResponse.access_token,
                });
                setError('Server Error');
            }
        },
    });

    const logOut = () => {
        setLogInfo({ ...logInfo, loggedIn: false, googledIn: false });
        localStorage.removeItem('jwtAuthToken');
        window.location.reload();
    };

    const submitLoginForm = async () => {
        const body = {
            accessToken: logInfo.token,
            ign: user.ign,
            steamId: user.steamId,
        };
        console.log(body);
        try {
            const response = await postRequest('/login', body);
            console.log('Second request response:');
            console.log(response);
            if (response.status === 200 && response.data.success) {
                console.log(response.data);
                setUser({
                    ...user,
                    ign: response.data.data.ign,
                    steamId: response.data.data.steamId,
                    pic: response.data.data.picture,
                    email: response.data.data.email,
                    name: response.data.data.name,
                });
                setLogInfo({
                    ...logInfo,
                    loggedIn: true,
                });
            } else {
                console.log(
                    `Second request not 200: ${JSON.stringify(
                        response.data?.message
                    )}`
                );
                setError(response.data?.message);
            }
        } catch (err) {
            console.log(
                `Second Request: error submitting: ${JSON.stringify(err)}`
            );
            setError('Server Error');
        }
    };

    const closeModal = () => {
        setLogInfo({ ...logInfo, googledIn: false });
        setError('');
    };

    if (logInfo.loggedIn) {
        return (
            <NavDropdown
                align='end'
                title={
                    <div>
                        <img
                            width='40px'
                            style={{ borderRadius: '50%' }}
                            src={user.pic}
                            alt='user pic'
                        />
                    </div>
                }
            >
                <Dropdown.Header>
                    <h5 className='text-center text-dark'>{user.ign}</h5>
                    {user.email}
                </Dropdown.Header>
                <Dropdown.Divider />
                <Dropdown.Item href='account'>Profile</Dropdown.Item>
                <Dropdown.Item>My Team</Dropdown.Item>
                <Dropdown.Item onClick={logOut}>
                    <i className='fa fa-sign-out'></i> Logout
                </Dropdown.Item>
            </NavDropdown>
        );
    }

    return (
        <div>
            {logInfo.googledIn && (
                <Modal
                    onSubmit={submitLoginForm}
                    closeModal={closeModal}
                    user={user}
                    setUser={setUser}
                    errorMessage={error}
                />
            )}
            <div>
                <button
                    onClick={() => login()}
                    id='google-button'
                    className='btn btn-outline-dark'
                    disabled={logInfo.googledIn}
                >
                    <img
                        width='20px'
                        style={{ marginBottom: '3px', marginRight: '5px' }}
                        alt=''
                        src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png'
                    />
                    Log in with Google
                </button>
            </div>
        </div>
    );
};

export default Login;
