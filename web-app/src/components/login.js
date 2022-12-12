import { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const Login = () => {
    const [state, setState] = useState({tokenReceived: false, loggedIn: false, ign: '', steamId: '', errorLogging: false, error: '', pic: ''}) 

    const login = useGoogleLogin({
        onSuccess: async tokenResponse  => {
            const body = {
                accessToken: tokenResponse.access_token,
            }
            try {
                const response = await axios.post("http://26.47.157.189:5000/login", body)
                console.log(response.data);
                if(response.status === 200 && response.data.success) {
                    setState({
                        ...state, 
                        loggedIn: true, 
                        ign: response.data.data.ign, 
                        steamId: response.data.data.steamId, 
                        pic: response.data.data.picture, 
                        tokenReceived: true, 
                        token: tokenResponse.access_token
                    })
                } else {
                    setState({...state, tokenReceived: true, token: tokenResponse.access_token})
                    console.log(response.data.message);
                }
            } catch (err) {
                console.log('error submitting')
                setState({...state, errorLogging: true, error: JSON.stringify(err), tokenReceived: true, token: tokenResponse.access_token})
            }
        }
    });

    const handleChange = (event) => {
        const target = event.target;
        console.log(state)
        if(target.name === 'ign') {
            setState({ ...state, ign: target.value})
        } else if(target.name === 'steamId') {
            setState({ ...state, steamId: target.value})
        }
    }

    const submitLoginForm = async () => {
        console.log('submitted')
        if(!state.tokenReceived) {
            console.log('not logged in')
        }
        const body = {
            accessToken: state.token,
            ign: state.ign,
            steamId: state.steamId,
        }
        console.log(body)
        try {
            const response = await axios.post("http://26.47.157.189:5000/login", body)
            console.log('sent')
            console.log(response.data);
            if(response.status === 200 && response.data.success) {
                console.log(response.data);
                setState({
                    ...state, 
                    loggedIn: true, 
                    ign: response.data.data.ign, 
                    steamId: response.data.data.steamId,  
                    pic: response.data.data.picture
                })
            }        
        } catch (err) {
            console.log('error submitting')
            setState({...state, errorLogging: true, error: JSON.stringify(err)})
        }
    }

    console.log(state);
    if(state.loggedIn) {
        return (
            <div>
                <h1>Welcome {state.ign} to mumbai</h1>
                <img src={state.pic} alt=""></img>
            </div>
        )
    }

    return state.tokenReceived ? (
                <div>
                    <label>IGN:</label>
                    <input name="ign" value = {state.ign} onChange = {handleChange}/>
                    <label>Steam Id:</label>
                    <input name="steamId" value = {state.steamId} onChange = {handleChange}/><br/>
                    {state.error}
                    <button onClick = {submitLoginForm}>Submit</button>
                </div>
        ) : (
        <div>
            <h1>mumbai</h1>
            <div>
            <button onClick={() => login()}>
            Sign in with Google 🚀{' '}
            </button>;
            </div>
        </div>
      );
}

export default Login;