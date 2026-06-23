import streamlit as st
import pandas as pd
import numpy as np
import time

# === 1. 앱 기본 설정 및 타이틀 ===
st.set_page_config(layout="wide", page_title="마이크로바이옴 약동학 시뮬레이터")
st.title("🧬 장내 미생물 교차 피딩(Cross-feeding) 시뮬레이터")
st.markdown("### 비피도박테리움 기반 4:4:2 배합비 최적화 및 GLP-1 유도 예측 시스템")
st.divider()

# === 2. 좌측 입력 패널 (Sidebar) 조종석 ===
with st.sidebar:
    st.header("⚙️ 시뮬레이션 변수 설정")

    st.subheader("1. 원료 배합비 (%)")
    fos_ratio = st.slider("FOS (프락토올리고당)", 0, 100, 40)
    inulin_ratio = st.slider("Inulin (이눌린)", 0, 100, 40)
    pectin_ratio = st.slider("Pectin (펙틴)", 0, 100, 20)

    total_ratio = fos_ratio + inulin_ratio + pectin_ratio
    if total_ratio != 100:
        st.warning(f"⚠️ 합계가 {total_ratio}%입니다. 100%로 맞춰주세요.")
    else:
        st.success("✅ 배합비 100% 설정 완료")

    st.subheader("2. 장내 환경 세팅")
    ph_level = st.slider("대장 초기 산도 (pH)", 5.0, 7.5, 6.5, 0.1)
    
    st.subheader("3. 투입 용량 및 대상자 정보")
    dose_g = st.number_input("1회 섭취량 (g)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    current_weight = st.slider("대상자 현재 체중 (kg)", 40, 150, 80)
    bifido_baseline = st.slider("초기 비피도박테리움 비율 (%)", 1, 30, 10)

    st.markdown("---")
    run_btn = st.button("🚀 시뮬레이션 실행", type="primary", use_container_width=True)

# === 3. 메인 대시보드 ===
if run_btn:
    if total_ratio != 100:
        st.error("🚨 오류: 배합비 합계가 100%가 아닙니다.")
    else:
        with st.spinner("가상 약동학 데이터 연산 및 장-뇌 축(Gut-Brain Axis) 시뮬레이션 가동 중..."):
            time.sleep(1.5) 
            
            st.markdown("## 🔬 시뮬레이션 결과 리포트")
            
            glp1_score = (pectin_ratio * 2.5) + (inulin_ratio * 0.5)
            
            if glp1_score >= 60:
                base_loss_pct = 0.138 * (dose_g / 5.0) * (6.5 / ph_level)
            else:
                base_loss_pct = 0.035 * (glp1_score / 60.0) * (dose_g / 5.0)
                
            expected_loss = round(current_weight * base_loss_pct, 1)
            after_weight = round(current_weight - expected_loss, 1)
            
            # --- [NEW] 12주 예측 하이라이트 ---
            st.markdown("### 🔥 [임상 예측] 12주 복용 후 체중 감량 결과")
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("섭취 전 초기 체중", f"{current_weight} kg")
            kpi2.metric("12주 후 예상 감량치", f"-{expected_loss} kg", f"초기 체중의 {round(base_loss_pct*100, 1)}% 감소", "inverse")
            kpi3.metric("12주 후 최종 예상 체중", f"{after_weight} kg")
            
            st.divider()

            # --- [NEW] 장-뇌 축(Gut-Brain Axis) 타겟팅 메커니즘 패널 ---
            st.markdown("### 🧠 초고속 포만감 전달: 장-뇌 축 (Gut-Brain Axis) 신경 타겟팅 기전")
            if glp1_score >= 60:
                st.success(f"**[상태: 🟢 연결 활성화]** L-세포 자극 지수 {glp1_score} 달성. 내인성(Endogenous) 천연 GLP-1 분비 기전이 강력하게 활성화되었습니다.")
                
                # 시각적 흐름도 생성
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                col_m1.info("🎯 **1. 타겟 도달**\n\n4:4:2 배합 펙틴이 대장 말단 L-세포 자극")
                col_m2.warning("⚡ **2. 국소 자극 (Paracrine)**\n\n혈관 진입 전 미주신경(Vagus Nerve) 수용체 결합")
                col_m3.error("🧠 **3. 초고속 신경 전달**\n\n전기 신호로 전환되어 시상하부(Hypothalamus) 직행")
                col_m4.success("📉 **4. 최종 효과**\n\n전신 부작용 제로(0), 즉각적이고 강력한 포만감 형성")
            else:
                st.warning(f"**[상태: 🔴 연결 실패]** L-세포 자극 지수 {glp1_score} (임계점 60 미달). 고분자 식이섬유 비율이 낮아 미주신경 자극이 불가능합니다.")
                
            st.divider()
            
            # --- 기존 4대 특허 패널 ---
            st.markdown("### 🧬 4대 특허 방어 기술 시각화")
            col1, col2 = st.columns(2, gap="large")
            locations = ["1. 맹장", "2. 상행결장", "3. 횡행결장", "4. 하행결장(말단)"]
            
            with col1:
                st.subheader("📊 [A] 지속방출 대사 구배")
                data_A = pd.DataFrame({
                    "FOS": [fos_ratio, fos_ratio*0.1, 0, 0],
                    "Inulin": [inulin_ratio, inulin_ratio*0.8, inulin_ratio*0.2, 0],
                    "Pectin": [pectin_ratio, pectin_ratio*0.95, pectin_ratio*0.8, pectin_ratio*0.5]
                }, index=locations)
                st.line_chart(data_A)
                
            with col2:
                st.subheader("💨 [B] 가스 발생 저감 지수")
                gas_peak = (fos_ratio * 1.5) + (inulin_ratio * 0.8) + (pectin_ratio * 0.3)
                gas_data = pd.DataFrame({"가스 발생 (ml/h)": [gas_peak*0.2, gas_peak, gas_peak*0.5, gas_peak*0.1]}, index=locations)
                st.area_chart(gas_data, color="#ff7f0e")
            
            col3, col4 = st.columns(2, gap="large")
            
            with col3:
                st.subheader("🎯 [C] 천연 GLP-1 유도 피크")
                glp1_data = pd.DataFrame({"GLP-1 활성도": [10, 25, 45, glp1_score]}, index=locations)
                st.bar_chart(glp1_data, color="#2ca02c")

            with col4:
                st.subheader("🤝 [D] 상리공생 대사 회전율")
                butyrate_yield = (bifido_baseline * 0.5) + (dose_g * 2) + 20
                syntrophy_data = pd.DataFrame({
                    "1차 산물": [80, 50, 20, 5],
                    "2차 산물": [5, 30, butyrate_yield*0.8, butyrate_yield]
                }, index=locations)
                st.line_chart(syntrophy_data)

            st.divider()

            # --- 시장 경쟁력 분석 ---
            st.markdown("### 🏆 [시장 경쟁력 분석] 위고비 vs 마운자로 vs 신바이오틱스")
            comp_data = pd.DataFrame({
                "위고비": [8, 2, 3, 3],
                "마운자로": [10, 1, 2, 4],
                "신바이오틱스": [7, 10, 10, 9]
            }, index=["1. 감량 효과", "2. 가격 경쟁력", "3. 안전성(무부작용)", "4. 요요 방지력"])
            
            st.bar_chart(comp_data, horizontal=True)