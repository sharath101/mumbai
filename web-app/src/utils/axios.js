import axios from 'axios';
import Constants from '../constants/common'


const postRequest = async (path, params = {}, hostUrl) => {
    try {
        if(!hostUrl) {
            hostUrl = Constants.SERVER_HOST.LOCAL;
        }
        const jwtAuthToken = localStorage.getItem('jwtAuthToken') || ''
        const response = await axios.post(`${hostUrl}${path}`, params, {
            headers: {
                "Authorization": `Bearer ${jwtAuthToken}`,
            }
        });
        console.log(response?.headers?.authorization);
        const token = response?.headers?.authorization.split(' ')[1];
        console.log(token);
        localStorage.setItem('jwtAuthToken', token);
        return response;
    } catch(err) {
        throw err;
    }
}asd

const getRequest = async (path, params = {}, hostUrl) => {
    try {
        if(!hostUrl) {
            hostUrl = Constants.SERVER_HOST.LOCAL;
        }
        const jwtAuthToken = localStorage.getItem('jwtAuthToken') || '';
        console.log('idk');
        const response = await axios.get(`${hostUrl}/${path}`, {
            params,
            headers: {
                "Authorization": `Bearer ${jwtAuthToken}`,
            }
        });
        console.log('idk2');
        return response;
    } catch(err) {
        throw err;
    }
}

export {
    postRequest,
    getRequest
}