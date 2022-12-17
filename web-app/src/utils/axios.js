import axios from 'axios';
import Constants from '../constants/common'


const postRequest = async (path, params, hostUrl) => {
    try {
        if(!hostUrl) {
            hostUrl = Constants.common.SERVER_HOST.LOCAL;
        }
        const response = await axios.post(`${hostUrl}/${path}`, params, {
            headers: {
                
            }
        });
    } catch(err) {
        throw err;
    }
    return response;
}

const getRequest = async (path, params, hostUrl) => {
    try {
        if(!hostUrl) {
            hostUrl = Constants.common.SERVER_HOST.LOCAL;
        }
        const response = await axios.get(`${hostUrl}/${path}`, {
            params,
            headers: {

            }
        });
    } catch(err) {
        throw err;
    }
    return response;
}