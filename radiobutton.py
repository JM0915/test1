import streamlit as st
import pandas as pd

def main() :

    df = pd.read_csv('samples (1).csv')
    # st.dataframe(df)

    # 체크박스 : 체크 해제/ 체크
    # 두개 동작중 하나를 한다. 체크하면 TRUE가 된다.

    if st.checkbox('헤드 5개 보기'):
        st.dataframe(df.head())
    else:
        st.text('헤드 숨겼습니다.')


if __name__ == "__main__" :
    main()