import streamlit as st
import cv2
from PIL import Image, ImageEnhance
import numpy as np

def main():
    st.title("이미지 변환 (Streamlit and OpenCV)")

    image_file = st.file_uploader("이미지 업로드",type=['jpg','png','jpeg'])

    feature_choice = st.sidebar.selectbox("변환 특징", ["GRAY","RGB"])

    if image_file is not None:

        our_image = Image.open(image_file)
        st.image(our_image, width = 600)

        if st.button("Process"):

            if feature_choice == 'GRAY':
                st.image(result_img,width = 600)
            elif feature_choice == 'RGB':
                result_img2 = canninze_image(our_image)
                st.image(result_img2,width=600)
    else:
        st.text('이미지를 선택하세요')

if __name__ == '__main__':
    main()
