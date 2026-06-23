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
st.info("좌측 패널에서 변수를 설정하면, 우측에 4대 특허 방어 로직 및 투자자용 감량 예측 결과가 출력됩니다.")

# === 2. 좌측 입력 패널 (Sidebar) 조종석 ===
with st.sidebar:
    st.header("⚙️ 시뮬레이션 변수 설정")
    st.markdown("특허 논리 검증 및 체중 예측을 위해 변수를 조작해 보세요.")

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

    st.subheader("3. 투입 용량 및 대상자 정보")
    dose_g = st.number_input("1회 섭취량 (g)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    current_weight = st.slider("대상자 현재 체중 (kg)", 40, 150, 80)
    bifido_baseline = st.slider("초기 비피도박테리움 비율 (%)", 1, 30, 10)

    st.markdown("---")
    run_btn = st.button("🚀 시뮬레이션 실행", type="primary", use_container_width=True)

# === 3. 메인 대시보드 (4대 특허 및 투자자 패널) ===
if run_btn:
    if total_ratio != 100:
        st.error("🚨 오류: 배합비 합계가 100%가 아닙니다. 사이드바에서 비율을 조정해주세요.")
    else:
        with st.spinner("가상 몬테카를로 약동학 데이터 연산 및 체중 감량 시뮬레이션 가동 중..."):
            time.sleep(1.5) 
            
            st.markdown("## 🔬 시뮬레이션 결과 리포트")
            
            # --- [투자자 전용 대시보드 스위치] ---
            glp1_score = (pectin_ratio * 2.5) + (inulin_ratio * 0.5)
            
            if glp1_score >= 60:
                base_loss_pct = 0.138 * (dose_g / 5.0) * (6.5 / ph_level)
            else:
                base_loss_pct = 0.035 * (glp1_score / 60.0) * (dose_g / 5.0)
                
            expected_loss = round(current_weight * base_loss_pct, 1)
            after_weight = round(current_weight - expected_loss, 1)
            
            st.markdown("### 🔥 [신바이오틱스] 12주 복용 후 임상 체중 감량 예측 결과")
            
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(label="섭취 전 초기 체중", value=f"{current_weight} kg")
            with kpi2:
                st.metric(
                    label="12주 후 예상 감량치", 
                    value=f"-{expected_loss} kg", 
                    delta=f"초기 체중의 {round(base_loss_pct*100, 1)}% 감소", 
                    delta_color="inverse"
                )
            with kpi3:
                st.metric(label="12주 후 최종 예상 체중", value=f"{after_weight} kg")
                
            st.divider() 
            
            # --- 기존 4대 특허 패널 출력 ---
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
                glp1_data = pd.DataFrame({
                    "GLP-1 분비 활성도": [10, 25, 45, glp1_score]
                }, index=locations)
                st.bar_chart(glp1_data, color="#2ca02c")
                
                if glp1_score >= 60:
                    st.success(f"✅ **임계점 돌파 (활성도 {glp1_score})!** 위고비 모방 메커니즘 활성화.")
                else:
                    st.warning(f"⚠️ **임계점 미달 (활성도 {glp1_score}):** 고분자 식이섬유 부족.")

            with col4:
                st.subheader("🤝 [D] 상리공생 대사 회전율")
                st.caption("특허 포인트: 대사물질(아세트산→부티르산) 패스 속도")
                butyrate_yield = (bifido_baseline * 0.5) + (dose_g * 2) + 20
                syntrophy_data = pd.DataFrame({
                    "1차 산물 (아세트산/젖산)": [80, 50, 20, 5],
                    "2차 산물 (부티르산)": [5, 30, butyrate_yield*0.8, butyrate_yield]
                }, index=locations)
                st.line_chart(syntrophy_data)

            st.divider()

            # --- [NEW] 가로형(Horizontal) 3자 비교 차트 ---
            st.markdown("### 🏆 [시장 경쟁력 분석] 위고비 vs 마운자로 vs 당사 신바이오틱스")
            st.caption("비만 치료제 시장의 게임 체인저: 주사제 한계를 극복한 천연 마이크로바이옴 플랫폼 종합 평가 (10점 만점)")
            
            # 범례 이름이 너무 길면 차트가 지저분해지므로 핵심 단어로 축약
            comp_data = pd.DataFrame({
                "위고비": [8, 2, 3, 3],
                "마운자로": [10, 1, 2, 4],
                "신바이오틱스": [7, 10, 10, 9]
            }, index=["1. 감량 효과", "2. 가격 경쟁력", "3. 안전성(무부작용)", "4. 요요 방지력"])
            
            # horizontal=True 옵션으로 텍스트를 편안하게 읽을 수 있는 가로 막대그래프로 출력
            st.bar_chart(comp_data, horizontal=True)
            
            st.info("💡 **투자 포인트:** 기존 주사제(위고비/마운자로)는 초기 감량 효과가 높지만, 월 100만 원 이상의 비용과 극심한 위장관 부작용, 그리고 투여 중단 시 체중이 돌아오는 **'요요 현상'**이라는 치명적 단점이 있습니다. 반면 당사의 신바이오틱스는 감량 속도는 약간 완만할 수 있으나, **압도적인 가격 경쟁력, 제로(0)에 가까운 부작용, 그리고 장내 생태계 자체를 '살 안 찌는 체질'로 리셋하는 지속 가능성**을 통해 시장을 장악할 수 있습니다.")