import streamlit as st
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import tensorflow as tf

import smtplib
from email.mime.text import MIMEText

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('kjm20174035@gmail.com', 'dwiypvzovyalqubj')


new_model = tf.keras.models.load_model('my_model.h5')
def load_image(img):
    im = Image.open(img)
    return im


def welcome():
    st.title('부정맥 판별')


    st.image('test.png', use_column_width=True)
    st.subheader('시간과 공간의 제약을 감소하고, 어디서든지 부정맥을 판별할 수 있어요')
    st.write('또 부정맥 여부만 확인하는게 아니라 어떤 종류의 부정맥인지와 대처방안도 함께 제시해줍니다.')


def photo():
    st.header("Arrhythmia Detection")

    image_file = st.file_uploader("부정맥 이미지를 업로드해주세요.", type=['jpg', 'png', 'jpeg'])
    if image_file is not None:
        st.image(image_file)
        img1 = Image.open(image_file)
        img_array = np.array(img1)

        my_img = cv2.resize(img_array, (200,200))
        my_img = np.reshape(my_img,(1,200,200,3))
        my_test = new_model(my_img)
        # st.write(my_test)

        result = np.argmax(my_test)
        #my_dict = {0:'진단결과 : 부정맥 (심방세동) 입니다. 가까운 병원에 방문해 진료를 받아보세요',
        #           1:'진단결과 : 이상 없습니다.',
        #           2:'진단결과 : 부정맥 (심실조기수축) 입니다. 가까운 병원에 방문해 진료를 받아보세요.',
        #           3:'진단결과 : 부정맥 (서맥) 입니다. 가까운 병원에 방문해 진료를 받아보세요.'}
        #st.write(my_dict.get(result))
        if result == 1:
             st.success('진단결과 : 이상 없습니다.')
             # 메일발송
             msg = MIMEText('내용 : 사용자에게 이상이 없습니다.')
             msg['Subject'] = '진단결과 : 사용자에게 이상이 없습니다.'
             s.sendmail("kjm20174035@gmail.com", "qnfvudqnfaks@naver.com", msg.as_string())
             s.quit()
             # 세션 끝
        elif result == 0:
             st.error('진단결과 : 심방세동(AFIB) 입니다. 가까운 병원에 방문해 진료를 받아보세요')
             st.header("심방세동을 진단받았다면, 병원에 가서 이러한 치료를 받으세요.")
             st.subheader("Synchronized Cardioversion, 동기화 심율동전환")
             st.warning("이 치료 전에 할 것")
             st.write("- 심방세동 상태가 얼마나 유지됐는지 확인한다. 오래 지속되었을 경우 혈전이 생길 수 있어 항응고치료가 필요할 수 있음")
             st.warning("이 치료 후에 할 것")
             st.write("- 일정 주기동안 항응고제 복용")
             st.write('--------------------------------------------------------------')
             st.subheader("Ablation 절제 : 비정상적인 전기발사를 보이는 심장 조직 부분을 파괴")
             st.write('--------------------------------------------------------------')
             st.subheader("Warfarin(와파린) 복용 - 항응고제")
             st.write('--------------------------------------------------------------')
             st.subheader('Beta-clockers, Calcium channel blockers 복용 : 심박수와 심장리듬을 조절해줍니다.')
             msg = MIMEText('사용자가 증상이 없는 안정된 상태라면 심박수만 관찰해도 충분합니다.\n\n'
                            '※ 약물/수술적 치료\n\n'
                            '동기화 심율동전환 수술\n'
                            'Ablation 절제\n'
                            'Warfarin(와파린) 복용\n'
                            'Beta-clockers, Calcium channel blockers 복용')
             msg['Subject'] = '진단결과 : 사용자에게 심방세동이 검출되었습니다.'
             s.sendmail("kjm20174035@gmail.com", "qnfvudqnfaks@naver.com", msg.as_string())
             s.quit()
        elif result == 2:
             st.error('진단결과 : 심실조기수축(PVC) 입니다. 가까운 병원에 방문해 진료를 받아보세요.')
             st.header("심실조기수축을 진단받았다면, 병원에 가서 이러한 치료를 받으세요.")
             st.write('--------------------------------------------------------------')
             st.subheader("심계항진이 있는 경우, Beta-clockers 베타 차단제, Calclum channel blockers 칼슘채널 차단제를 복용")
             st.warning("-위 약물들은 심장이 강하게 뛰지 않게 함")
             st.write('--------------------------------------------------------------')
             st.subheader("Radiofrequency Ablation 고주파 절제 시술")
             st.warning("-이소성 박동을 일으키는 조직을 파괴")
             msg = MIMEText('- 심계항진이 있는 경우, Beta-clockers(베타 차단제), Calcium channel blockers(칼슘채널 차단제)를 복용하세요.\n'
                            '  Radiofrequency Ablation 고주파 절제술을 받으세요')
             msg['Subject'] = '진단결과 : 심실조기수축이 검출되었습니다.'
             s.sendmail("kjm20174035@gmail.com", "qnfvudqnfaks@naver.com", msg.as_string())
             s.quit()
        elif result == 3:
             st.error('진단결과 : 서맥(SBR) 입니다. 가까운 병원에 방문해 진료를 받아보세요.')
             st.header("서맥을 진단받았다면, 병원에 가서 이러한 치료를 받으세요.")
             st.write('--------------------------------------------------------------')
             st.subheader("비약물성 중재")
             st.warning("-호흡 관찰하고, 필요시 산소 공급하기")
             st.warning("-폐, 심장소리 관찰하기")
             st.warning("-호르몬, 전해질 레벨 관찰")
             st.write('--------------------------------------------------------------')
             st.subheader("약물/수술적 치료")
             st.warning("-Atropine(아트로핀), Dopamine(도파민) 이나 Epinephrine(에피네프린) 등 복용하기")
             msg = MIMEText('약물을 사용하지 않을 때\n\n증상이 뚜렷하게 나타나지 않는다면 치료할 필요는 없습니다.\n'
                            '호흡을 관찰하고 필요하면 산소를 공급해 주세요.'
                            ' 폐, 심장소리, 호르몬, 전해질 레벨을 관찰하세요.\n\n'
                            '약물 / 수술적 치료\n\n'
                            '- Atropine(아트로핀), Dopamin(도파민), Epinephrine(에피네프린)을 복용하는 걸 추천드려요.')
             msg['Subject'] = '진단결과 : 사용자에게 서맥이 검출되었습니다.'
             s.sendmail("kjm20174035@gmail.com", "qnfvudqnfaks@naver.com", msg.as_string())
             s.quit()

        # st.write(np.round(my_test),4)
        # st.write(np.argmax(my_test))
#def Video():
#    st.header("심방세동을 진단받았다면, 병원에 가서 이러한 치료를 받으세요.")
#    st.subheader("Synchronized Cardioversion, 동기화 심율동전환")
#    st.warning("이 치료 전에 할 것")
#    st.write("- 심방세동 상태가 얼마나 유지됐는지 확인한다. 오래 지속되었을 경우 혈전이 생길 수 있어 항응고치료가 필요할 수 있음")
#    st.warning("이 치료 후에 할 것")
#    st.write("- 일정 주기동안 항응고제 복용")
#    st.write('--------------------------------------------------------------')
#    st.subheader("Ablation 절제 : 비정상적인 전기발사를 보이는 심장 조직 부분을 파괴")
#    st.write('--------------------------------------------------------------')
#    st.subheader("Warfarin(항응고제) 복용")
#    st.write('--------------------------------------------------------------')
#    st.subheader("Calcium channel blockers - 칼슘채널 차단제(심박수, 심장리듬을 조절) 복용")



    enhance_type = st.sidebar.radio("Enhance Type",["부정맥 검사"])
    if enhance_type == 'Gray-Scale':
        new_img = np.array(our_image.convert('RGB'))
        img = cv2.cvtColor(new_img,1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # st.write(new_img)
        st.image(gray)
    if enhance_type == 'Contrast':
        c_rate = st.sidebar.slider("Contrast",0.5,3.5)
        enhancer = ImageEnhance.Contrast(our_image)
        img_output = enhancer.enhance(c_rate)
        st.image(img_output)
    if enhance_type == 'Brightness':
        c_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
        enhancer = ImageEnhance.Brightness(our_image)
        img_output = enhancer.enhance(c_rate)
        st.image(img_output)
    if enhance_type == 'Blurring':
        new_img = np.array(our_image.convert('RGB'))
        blu_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
        img = cv2.cvtColor(new_img, 1)
        blu_img = cv2.GaussianBlur(img, (11,11),blu_rate)
        # st.write(new_img)
        st.image(blu_img)

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # x = st.slider('Change Threshold value', min_value=50, max_value=255)
        # ret, thresh1 = cv2.threshold(image, x, 255, cv2.THRESH_BINARY)
        # thresh1 = thresh1.astype(np.float64)
        # st.image(thresh1, use_column_width=True, clamp=True)

   # else:
        #st.text("이미지를 넣어주세요.")


#
#
# if st.button('See Original Image of Tom'):
#     image_file = st.file_uploader("이미지 업로드", type=['jpg', 'png', 'jpeg'])
#     original = Image.open(image_file)
#     st.image(original, use_column_width=True)
#
# image = cv2.imread('AFIB1.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# x = st.slider('Change Threshold value', min_value=50, max_value=255)
# ret, thresh1 = cv2.threshold(image, x, 255, cv2.THRESH_BINARY)
# thresh1 = thresh1.astype(np.float64)
# st.image(thresh1, use_column_width=True, clamp=True)
#
# st.text("Bar Chart of the image")
# histr = cv2.calcHist([image], [0], None, [256], [0, 256])
# st.bar_chart(histr)
#
# st.text("Press the button below to view Canny Edge Detection Technique")
# if st.button('Canny Edge Detector'):
#     image = load_image("AFIB1.png")
#     edges = cv2.Canny(image, 50, 300)
#     cv2.imwrite('edges.jpg', edges)
#     st.image(edges, use_column_width=True, clamp=True)
#
# y = st.slider('Change Value to increase or decrease contours', min_value=50, max_value=255)
#
# if st.button('Contours'):
#     im = load_image("AFIB1.jpg")
#
#     imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#     ret, thresh = cv2.threshold(imgray, y, 255, 0)
#     image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     img = cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
#
#     st.image(thresh, use_column_width=True, clamp=True)
#     st.image(img, use_column_width=True, clamp=True)
#

def main():
    selected_box = st.sidebar.selectbox(
        '목록을 선택하세요',
        ('Main', '부정맥 검사')
    )


    if selected_box == 'Main':
        welcome()
    if selected_box == '부정맥 검사':
        photo()
    #if selected_box == '심방세동(AFIB)':
    #     Video()
    # if selected_box == 'Face Detection':
    #     face_detection()
    # if selected_box == 'Feature Detection':
    #     feature_detection()
    # if selected_box == 'Object Detection':
    #     object_detection()

if __name__ == '__main__':
    main()


# def welcome():
#     st.title('Image Processing using Streamlit')
#
#     st.subheader('A simple app that shows different image processing algorithms. You can choose the options'
#                  + ' from the left. I have implemented only a few to show how it works on Streamlit. ' +
#                  'You are free to add stuff to this app.')
#
#     st.image('hackershrine.jpg', use_column_width=True)
#
#
# def photo():
#     st.header("Thresholding, Edge Detection and Contours")
#
#
# if st.button('See Original Image of Tom'):
#     image_file = st.file_uploader("이미지 업로드", type=['jpg', 'png', 'jpeg'])
#     original = Image.open(image_file)
#     st.image(original, use_column_width=True)
#
# image = cv2.imread('AFIB1.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# x = st.slider('Change Threshold value', min_value=50, max_value=255)
# ret, thresh1 = cv2.threshold(image, x, 255, cv2.THRESH_BINARY)
# thresh1 = thresh1.astype(np.float64)
# st.image(thresh1, use_column_width=True, clamp=True)
#
# st.text("Bar Chart of the image")
# histr = cv2.calcHist([image], [0], None, [256], [0, 256])
# st.bar_chart(histr)
#
# st.text("Press the button below to view Canny Edge Detection Technique")
# if st.button('Canny Edge Detector'):
#     image = load_image("AFIB1.png")
#     edges = cv2.Canny(image, 50, 300)
#     cv2.imwrite('edges.jpg', edges)
#     st.image(edges, use_column_width=True, clamp=True)
#
# y = st.slider('Change Value to increase or decrease contours', min_value=50, max_value=255)
#
# if st.button('Contours'):
#     im = load_image("AFIB1.jpg")
#
#     imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#     ret, thresh = cv2.threshold(imgray, y, 255, 0)
#     image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     img = cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
#
#     st.image(thresh, use_column_width=True, clamp=True)
#     st.image(img, use_column_width=True, clamp=True)
