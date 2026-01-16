import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 한글 폰트 설정 (그래프 깨짐 방지) ---
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="무역통계 분석기", layout="wide")
st.title("📊 엑셀 데이터 무역통계 분석기")

# [중요] 사용하시는 파일의 실제 이름을 아래에 적어주세요. 
# 파일이 코드가 있는 폴더와 같은 위치에 있어야 합니다.
file_name = 'K-stat 무역통계 - 한국무역협회.xls' 

try:
    # 1. 엑셀 파일 읽기
    # K-stat 엑셀은 보통 상단 2~3줄이 제목이므로 skiprows로 건너뜁니다.
    df = pd.read_excel(file_name, skiprows=3) 

    # 2. 컬럼명 강제 지정 (K-stat 엑셀 구조 기준)
    # 데이터 구조에 따라 컬럼 개수가 다를 수 있으니 확인이 필요합니다.
    df.columns = ['년월', '수출금액', '수출증감률', '수입금액', '수입증감률', '무역수지']

    # 3. 데이터 전처리
    # '년월' 컬럼에서 '2024년'처럼 '년'이 포함된 행만 남기고 합계/비고 행은 삭제
    df = df[df['년월'].str.contains('년', na=False)].copy()

    # 숫자 데이터에 콤마(,)가 있거나 문자로 인식된 경우 숫자로 변환
    for col in ['수출금액', '수입금액', '무역수지']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    st.success(f"✅ '{file_name}' 파일을 성공적으로 분석했습니다.")

    # 4. 시각화 (그래프)
    st.subheader("📈 연도별 수출입 추이")
    
    # 시간 순서대로 보여주기 위해 데이터 순서 반전
    df_plot = df.iloc[::-1].reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df_plot, x='년월', y='수출금액', marker='o', label='수출금액', ax=ax, color='blue')
    sns.lineplot(data=df_plot, x='년월', y='수입금액', marker='o', label='수입금액', ax=ax, color='red')
    
    plt.xticks(rotation=45)
    plt.title("수출입 변동 현황 (단위: 백만불)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    st.pyplot(fig)

    # 5. 데이터 표 출력
    st.subheader("📋 상세 데이터")
    st.dataframe(df)

except FileNotFoundError:
    st.error(f"❌ '{file_name}' 파일을 찾을 수 없습니다. 파일명이 정확한지, 코드와 같은 폴더에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"❌ 에러 발생: {e}")
    st.info("팁: 엑셀 파일의 실제 구조에 따라 'skiprows' 숫자나 컬럼명을 조정해야 할 수 있습니다.")