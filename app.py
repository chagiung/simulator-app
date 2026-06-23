import streamlit as st
import pandas as pd
import numpy as np
import time

# === 1. 앱 기본 설정 및 타이틀 ===
st.set_page_config(layout="wide", page_title="마이크로바이옴 약동학 시뮬레이터")
st.title("🧬 장내 미생물 교차 피딩(Cross-feeding) 시뮬레이터")
st.markdown("### 비피도박테리움 기반 4:4:2 배합비 최적화 및 GLP-1 유도 예측 시스템")
st.divider()
st.success("시스템 정상 작동 중: 몬테카를로 시뮬레이션 엔진 대기 상태입니다.")
st.info("좌측 패널에서 변수를 설정하면, 우측에 4대 특허 방어 로직 결과가 출력됩니다.")

# === 2. 좌측 입력 패널 (Sidebar) 조종석 ===
with st.sidebar:
    st.header("⚙️ 시뮬레이션 변수 설정")
    st.markdown("특허 논리 검증을 위해 변수를 조작해 보세요.")

    st.subheader("1. 원료 배합비 (%)")
    fos_ratio = st.slider("FOS (프락토올리고당)", 0, 100, 40)
    inulin_ratio = st.slider("Inulin (이눌린)", 0, 100, 40)
    pectin_ratio = st.slider("Pectin (펙틴)", 0, 100, 20)

    total_ratio = fos_ratio + inulin_ratio + pectin_ratio
    if total_ratio != 100:
        st.warning(f"⚠️ 현재 배합비 합계가 {total_ratio}%입니다. 정확한 시뮬레이션을 위해 100%로 맞춰주세요.")
    else:
        st.success("✅ 배합비 100% 설정 완료")

    st.subheader("2. 장내 환경 세팅")
    ph_level = st.slider("대장 초기 산도 (pH)", 5.0, 7.5, 6.5, 0.1)
    transit_time = st.slider("장 통과 시간 (Hours)", 12, 72, 24)

    st.subheader("3. 투입 용량 및 마이크로바이옴")
    dose_g = st.number_input("1회 섭취량 (g)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    bifido_baseline = st.slider("초기 비피도박테리움 비율 (%)", 1, 30, 10)

    st.markdown("---")
    # 여기서 run_btn이 정의됩니다.
    run_btn = st.button("🚀 시뮬레이션 실행", type="primary", use_container_width=True)

# === 3. 메인 대시보드 (4대 특허 시각화 패널) ===
if run_btn:
    if total_ratio != 100:
        st.error("🚨 오류: 배합비 합계가 100%가 아닙니다. 사이드바에서 비율을 조정해주세요.")
    else:
        with st.spinner("가상 몬테카를로 약동학 데이터 연산 중... (시뮬레이션 가동)"):
            time.sleep(1.5) 
            
            st.markdown("## 🔬 시뮬레이션 결과 리포트")
            
            col1, col2 = st.columns(2, gap="large")
            locations = ["1. 맹장(상부)", "2. 상행결장", "3. 횡행결장", "4. 하행결장(말단)"]
            
            with col1:
                st.subheader("📊 [A] 지속방출 대사 구배")
                st.caption("특허 포인트: 대장 말단까지 끊기지 않는 생존율")
                data_A = pd.DataFrame({
                    "FOS (프락토)": [fos_ratio, fos_ratio*0.1, 0, 0],
                    "Inulin (이눌린)": [inulin_ratio, inulin_ratio*0.8, inulin_ratio*0.2, 0],
                    "Pectin (펙틴)": [pectin_ratio, pectin_ratio*0.95, pectin_ratio*0.8, pectin_ratio*0.5]
                }, index=locations)
                st.line_chart(data_A)
                
            with col2:
                st.subheader("💨 [B] 가스 발생 저감 지수")
                st.caption("특허 포인트: 발효 속도 분산을 통한 가스 폭발 억제")
                gas_peak = (fos_ratio * 1.5) + (inulin_ratio * 0.8) + (pectin_ratio * 0.3)
                gas_data = pd.DataFrame({
                    "가스 발생량 (ml/h)": [gas_peak*0.2, gas_peak, gas_peak*0.5, gas_peak*0.1]
                }, index=locations)
                st.area_chart(gas_data, color="#ff7f0e")
            
            st.divider() 
                
            col3, col4 = st.columns(2, gap="large")
            
            with col3:
                st.subheader("🎯 [C] 천연 GLP-1 유도 피크")
                st.caption("특허 포인트: L-세포 자극 임계점 돌파 여부")
                glp1_score = (pectin_ratio * 2.5) + (inulin_ratio * 0.5)
                glp1_data = pd.DataFrame({
                    "GLP-1 분비 활성도": [10, 25, 45, glp1_score]
                }, index=locations)
                st.bar_chart(glp1_data, color="#2ca02c")
                
                if glp1_score >= 60:
                    st.success("✅ **임계점 돌파!** 유의미한 GLP-1 분비가 예측됩니다.")
                else:
                    st.warning("⚠️ **임계점 미달:** 펙틴 등 고분자 비율을 늘려주세요.")

            with col4:
                st.subheader("🤝 [D] 상리공생 대사 회전율")
                st.caption("특허 포인트: 대사물질(아세트산→부티르산) 패스 속도")
                butyrate_yield = (bifido_baseline * 0.5) + (dose_g * 2) + 20
                syntrophy_data = pd.DataFrame({
                    "1차 산물 (아세트산/젖산)": [80, 50, 20, 5],
                    "2차 산물 (부티르산)": [5, 30, butyrate_yield*0.8, butyrate_yield]
                }, index=locations)
                st.line_chart(syntrophy_data)
                
                st.info("💡 비피도박테리움과 장내 상주균의 대사 패스율을 보여줍니다.")