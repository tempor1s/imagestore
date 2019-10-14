import {
    CREATE_IMAGE,
    GET_IMAGE,
    CLEAR_CURRENT,
    GET_IMAGES,
    UPDATE_IMAGE,
    DELETE_IMAGE,
    IMAGE_ERROR,
    SET_LOADING
} from '../types';

export default (state, action) => {
    switch (action.type) {
        case CREATE_IMAGE:
            return {}
        case GET_IMAGE:
            return {}
        case GET_IMAGES:
            return {}
        case UPDATE_IMAGE:
            return {}
        case DELETE_IMAGE:
            return {}
        case IMAGE_ERROR:
            return {}
        case SET_LOADING:
            return {
                ...state,
                loading: true
            }
        default:
            return state;
    }
};