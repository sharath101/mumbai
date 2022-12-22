import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Loader from '../components/loader';
import Settings from '../components/settings';

const Router = ({ user, setUser, logInfo, setLogInfo }) => {
    return (
        <React.Suspense fallback={<Loader />}>
            <Routes>
                <Route element={<div></div>} exact path='/' />
                <Route
                    element={<Settings user={user} setUser={setUser} />}
                    exact
                    path='/account'
                />
            </Routes>
        </React.Suspense>
    );
};

export default Router;
