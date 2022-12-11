import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys
import tensorflow as tf
import keras
import streamlit as st
from PIL import Image
from keras.models import load_model
Image = Image.open('AFIB1.png')
def main():
    st.title('웹 대시보드')
    print('Python version : ' , sys.version)
    print('Tensorflow version : ' , tf.__version__)
    print('Keras Version : ' , keras.__version__)


    model = load_model('my_model.h5')

    model.summary()

    st.image(Image, caption='aa')
if __name__ == '__main__':
    main()