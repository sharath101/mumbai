import { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const Login = () => {
    const [error, setError] = useState('');
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

    const submitLoginForm = async () => {
        const body = {
            accessToken: user.token,
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
    console.log(logInfo)
    if(logInfo.loggedIn) {
        return (
            <div>
                <h1>Welcome {user.ign} to mumbai</h1>
                <img src={user.pic} alt=""></img>
            </div>
        )
    }

    if(logInfo.googleIn){
        console.log('afdfas')
        return (
                <div>
                    <label>IGN:</label>
                    <input name="ign" value = {user.ign} onChange = {ev => setUser({...user, ign: ev.target.value})}/>
                    <label>Steam Id:</label>
                    <input name="steamId" value = {user.steamId} onChange = {ev => setUser({...user, steamId: ev.target.value})}/><br/>
                    {error}<br/>
                    <button onClick = {submitLoginForm}>Submit</button>
                </div>
        )
    }
    return (
        <div>
            <h1>mumbai</h1>
            <div>
            <button onClick={() => login()}>
            <h2>Sign in with Google 🚀{' '}</h2>
            {error}
            </button>
            </div>
        </div>
      );
}

export default Login;