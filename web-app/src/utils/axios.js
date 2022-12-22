import axios from 'axios';
import Constants from '../constants/common';

const postRequest = async (path, params = {}, hostUrl) => {
    try {
        if (!hostUrl) {
            hostUrl = Constants.SERVER_HOST.LOCAL;
        }
        const jwtAuthToken = localStorage.getItem('jwtAuthToken') || '';
        const response = await axios.post(`${hostUrl}${path}`, params, {
            headers: {
                Authorization: `Bearer ${jwtAuthToken}`,
            },
        });
        if (response?.headers?.authorization) {
            const token = response?.headers?.authorization.split(' ')[1];
            localStorage.setItem('jwtAuthToken', token);
        }
        return response;
    } catch (err) {
        throw err;
    }
};

const getRequest = async (path, params = {}, hostUrl) => {
    try {
        if (!hostUrl) {
            hostUrl = Constants.SERVER_HOST.LOCAL;
        }
        const jwtAuthToken = localStorage.getItem('jwtAuthToken') || '';
        const response = await axios.get(`${hostUrl}/${path}`, {
            params,
            headers: {
                Authorization: `Bearer ${jwtAuthToken}`,
            },
        });
        if (response?.headers?.authorization) {
            const token = response?.headers?.authorization.split(' ')[1];
            localStorage.setItem('jwtAuthToken', token);
        }
        return response;
    } catch (err) {
        throw err;
    }
};

const putRequest = async (path, params = {}, hostUrl) => {
    try {
        if (!hostUrl) {
            hostUrl = Constants.SERVER_HOST.LOCAL;
        }
        const jwtAuthToken = localStorage.getItem('jwtAuthToken') || '';
        const response = await axios.put(`${hostUrl}${path}`, params, {
            headers: {
                Authorization: `Bearer ${jwtAuthToken}`,
            },
        });
        if (response?.headers?.authorization) {
            const token = response?.headers?.authorization.split(' ')[1];
            localStorage.setItem('jwtAuthToken', token);
        }
        return response;
    } catch (err) {
        throw err;
    }
};

export { postRequest, getRequest, putRequest };
