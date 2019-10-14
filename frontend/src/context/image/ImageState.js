import React, { useReducer } from 'react';
import axios from 'axios';
import ImageContext from './imageContext';
import ImageReducer from './imageReducer';

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

const ImageState = props => {
    const initalState = {
        images: [],
        current: null, // Single image that is currently being viewed
        error: null,
        loading: false
    };

    const [state, dispatch] = useReducer(ImageReducer, initalState);

    const getImages = async () => {};

    const getImage = async imageId => {};

    const createImage = async image => {};

    const deleteImage = async imageId => {};

    const updateImage = async imageId => {};

    const setCurrent = async imageId => {};

    return (
        <ImageContext.Provider
            value={{
                images: state.images,
                current: state.current,
                error: state.error,
                loading: state.loading,
                getImages,
                getImage,
                createImage,
                deleteImage,
                updateImage,
                setCurrent
            }}
        >
            {props.children}
        </ImageContext.Provider>
    );
};

export default ImageState;