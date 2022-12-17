import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const UserForm = ({
    onSubmit,
    user,
    setUser,
    errorMessage
}) => {
    return (
        
        <Form>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label><b>IGN</b></Form.Label>
                <Form.Control type="text" placeholder="Enter IGN" onChangeCapture={ev => setUser({...user, ign: ev.target.value})}/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label><b>Steam Profile</b></Form.Label>
                <Form.Control type="text" placeholder="Enter Steam Profile URL" onChangeCapture={ev => setUser({...user, steamId: ev.target.value})}/>
                <Form.Text className="text-danger" >
                {errorMessage}
                </Form.Text>
            </Form.Group>
            <Button variant="primary" type="submit" onClick={onSubmit}>
                Submit
            </Button>
            {/* <div>
                <div>
                    <label>IGN</label><br/>
                    <input type="text" id="ign" onChange={ev => setUser({...user, ign: ev.target.value})}></input>
                </div>
                <div>
                    <label>Steam ID</label><br/>
                    <input type="text" id="steamId" onChange={ev => setUser({...user, steamId: ev.target.value})}></input>
                </div>
                <div>{errorMessage}</div>
                <div>
                    <button onClick = {onSubmit}>Submit</button>
                </div>
        </div> */}
        </Form>

    )
}

export default UserForm;