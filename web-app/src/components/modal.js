import ReactDOM from 'react-dom';
import UserForm from './form';

const Modal = ({ onSubmit, closeModal, user, setUser, errorMessage }) => {
    return ReactDOM.createPortal(
        <div className='modal-area' style={{ borderRadius: '5%' }}>
            <button className='_modal-close' onClick={closeModal}>
                <svg className='_modal-close-icon' viewBox='0 0 40 40'>
                    <path d='M 10,10 L 30,30 M 30,10 L 10,30' />
                </svg>
            </button>
            <UserForm
                onSubmit={onSubmit}
                user={user}
                setUser={setUser}
                errorMessage={errorMessage}
            />
        </div>,
        document.body
    );
};

export default Modal;
