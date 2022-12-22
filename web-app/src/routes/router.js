import React from 'react';
import { Route } from 'react-router-dom';
import Loader from '../components/loader';
import Settings from '../components/settings';

const Routes = ({ user, setUser, logInfo, setLogInfo }) => {
    return (
        <React.Suspense fallback={<Loader />}>
            <Routes>
                <Route>
                    element = {<div></div>}
                    exact path='/'
                </Route>
                <Route>
                    element=
                    {<Settings user={user} setUser={setUser} />}
                    exact path='/account'
                </Route>
            </Routes>
        </React.Suspense>
    );
};

export default Routes;
