import { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import Modal from './modal';
import Dropdown from 'react-bootstrap/Dropdown';
import NavDropdown from 'react-bootstrap/NavDropdown';
// import MenuItem from 'react-bootstrap/MenuItem';

const Login = () => {
    const [error, setError] = useState('');
    const [picClick, setPicClick] = useState(false);
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

    const login = useGoogleLogin({
        onSuccess: async tokenResponse  => {
            const body = {
                accessToken: tokenResponse.access_token,
            }
            try {
                const response = await axios.post("http://26.47.157.189:5000/login", body)
                console.log("First request response:");
                console.log(response);
                if(response.status === 200 && response.data.success) {
                    setUser({
                        ...user, 
                        ign: response.data.data.ign, 
                        steamId: response.data.data.steamId, 
                        pic: response.data.data.picture, 
                        email: response.data.data.email,
                        name:  response.data.data.name,
                    })
                    setLogInfo({
                        ...logInfo,
                        loggedIn: true, 
                        googledIn: true, 
                        token: tokenResponse.access_token
                    })
                    console.log(`Logged into app`);
                } else {
                    setLogInfo({...logInfo, googledIn: true, token: tokenResponse.access_token})
                    console.log(`Logged in with google alone`);
                }
            } catch (err) {
                console.log(`Error logging with google: ${JSON.stringify(err)}`)
                setLogInfo({...logInfo, googleIn: false, token: tokenResponse.access_token})
                setError('Server Error');
            }
        }
    });

    const logOut = () => {
        setLogInfo({...logInfo, loggedIn: false, googledIn: false})
        window.location.reload()
    }

    const submitLoginForm = async () => {
        const body = {
            accessToken: logInfo.token,
            ign: user.ign,
            steamId: user.steamId,
        }
        console.log(body)
        try {
            const response = await axios.post("http://26.47.157.189:5000/login", body)
            console.log("Second request response:");
            console.log(response);
            if(response.status === 200 && response.data.success) {
                console.log(response.data);
                setUser({
                    ...user, 
                    ign: response.data.data.ign, 
                    steamId: response.data.data.steamId, 
                    pic: response.data.data.picture, 
                    email: response.data.data.email,
                    name:  response.data.data.name,
                })
                setLogInfo({
                    ...logInfo,
                    loggedIn: true,
                })
            } else {
                console.log(`Second request not 200: ${JSON.stringify(response.data?.message)}`)
                setError(response.data?.message)
            }    
        } catch (err) {
            console.log(`Second Request: error submitting: ${JSON.stringify(err)}`)
            setError("Server Error")
        }
    }

    const closeModal = () => {
        setLogInfo({...logInfo, googledIn: false})
        setError('')
    }


    console.log(logInfo)
    if(logInfo.loggedIn) {
        console.log(picClick)
        return (
            <NavDropdown 
                title={
                    <div>
                        {user.ign}
                        <img width="40px" style={{borderRadius:"50%"}}
                            src={user.pic} 
                            alt="user pic"
                        />
                    </div>
                } 
                >

                <Dropdown.Item >Profile</Dropdown.Item>
                <Dropdown.Item onClick={logOut}>
                    <i className="fa fa-sign-out"></i> Logout
                </Dropdown.Item>
            </NavDropdown>
            // {/* <Dropdown>
            //     <Dropdown.Toggle variant="info" id="dropdown-basic">
            //     <img width="30px" style={{borderRadius:"50%"}} alt="" src={user.pic} />
            //     </Dropdown.Toggle>

            //     <Dropdown.Menu>
            //         <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
            //         <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
            //         <Dropdown.Item href="#/action-3" onClick={logOut}>Log Out</Dropdown.Item>
            //     </Dropdown.Menu>
            // </Dropdown> */}

        )
    }

    if(logInfo.googledIn){
        return (
                <div>
                <Modal
                    onSubmit = {submitLoginForm}
                    closeModal = {closeModal}
                    user = {user}
                    setUser = {setUser}
                    errorMessage = {error}
                />
                <div>
                    <button onClick={() => login()} id = "google-button" className ="btn btn-outline-dark" disabled={logInfo.googledIn} >
                        <img width="20px" style={{marginBottom:"3px", marginRight:"5px"}} alt="" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" />
                        Log in with Google
                    </button>
                </div>
            </div>
        )
    }
    return (
        <div>
            <button onClick={() => login()} id = "google-button" className ="btn btn-outline-dark" disabled={logInfo.googledIn} >
                <img width="20px" style={{marginBottom:"3px", marginRight:"5px"}} alt="" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" />
                Log in with Google
            </button>
        </div>
      );
}

export default Login;