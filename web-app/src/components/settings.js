import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useState } from 'react';
import { putRequest } from '../utils/axios';

const Settings = ({ user, setUser }) => {
    const [error, setError] = useState('');
    const [tempUser, setTempUser] = useState({
        ign: '',
        steamId: '',
    });

    const updateProfile = async () => {
        const body = {
            ign: tempUser.ign === '' ? user.ign : tempUser.ign,
            steamId: tempUser.steamId === '' ? user.steamId : tempUser.steamId,
        };
        console.log(body);
        try {
            const response = await putRequest('/profile', body);
            console.log('Update profile request response:');
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
            } else {
                console.log(
                    `Update profile not 200: ${JSON.stringify(
                        response.data?.message
                    )}`
                );
                setError(response.data?.message);
            }
        } catch (err) {
            console.log(
                `Update profile: Error submitting: ${JSON.stringify(err)}`
            );
            setError('Server Error');
        }
    };

    return (
        <div className='container-fluid col-md-10'>
            <div
                className='card mt-5 bg-dark text-white'
                style={{ height: '80vh' }}
            >
                <div className='card-header align'>
                    <h1>Update Profile</h1>
                </div>
                <div className='card-body'>
                    <Form>
                        <Form.Group className='mb-3'>
                            <Form.Label>
                                <b>Change IGN</b>
                            </Form.Label>
                            <Form.Control
                                type='text'
                                placeholder='Enter IGN'
                                onChangeCapture={(ev) =>
                                    setTempUser({
                                        ...tempUser,
                                        ign: ev.target.value,
                                    })
                                }
                            />
                        </Form.Group>
                        <br />
                        <Form.Group className='mb-3'>
                            <Form.Label>
                                <b>Change Steam Profile</b>
                            </Form.Label>
                            <Form.Control
                                type='text'
                                placeholder='Enter Steam Profile URL'
                                onChangeCapture={(ev) =>
                                    setTempUser({
                                        ...tempUser,
                                        steamId: ev.target.value,
                                    })
                                }
                            />
                            <Form.Text className='text-danger'>
                                {error}
                            </Form.Text>
                        </Form.Group>
                        <br />
                        <Button
                            variant='primary'
                            className='float-right'
                            onClick={updateProfile}
                        >
                            Submit
                        </Button>
                    </Form>
                </div>
            </div>
        </div>
    );
};

export default Settings;
