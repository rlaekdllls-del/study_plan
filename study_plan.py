import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 3-(1). 데이터 구조 (리스트) : 기간 및 과목별 추천 공부법 정의
# ---------------------------------------------------------
# 3일 이하 남았을 때 (단기 벼락치기 전략)
short_term_steps = ["1단계 (핵심압축)", "2단계 (실전적용)", "3단계 (최종점검)"]
short_term_methods = {
    "국어": ["수업 필기 및 핵심 지문 3회독", "학교 기출문제 및 오답 선지 분석", "문학 작품별 핵심 주제 백지 복습"],
    "수학": ["공식 및 필수 개념 30분 총정리", "틀렸던 문제(오답)만 다시 풀기", "교과서/프린트 예제 문제 빠른 스캔"],
    "영어": ["본문 해석 및 핵심 문법 포인트 암기", "변형 문제 및 기출 빈출 유형 풀이", "헷갈리는 영단어/숙어 최종 암기"],
    "과학": ["핵심 개념 프린트 및 도표 암기", "기출문제 풀이 및 오답 개념 확인", "실험 과정 및 결과 백지 테스트"]
}

# 4일 이상 남았을 때 (중장기 정석 전략)
long_term_steps = ["1단계 (개념완성)", "2단계 (유형훈련)", "3단계 (심화/오답)"]
long_term_methods = {
    "국어": ["교과서 및 자습서 정독 후 구조화", "비문학/문학 유형별 문제집 풀이", "오답 노트 작성 및 낯선 지문 대비"],
    "수학": ["개념서 정독 및 기본 원리 이해", "유형별 문제집 단계별 풀이", "고난도 심화 문제 도전 및 오답 정리"],
    "영어": ["문장 구조 분석 및 구문 독해 연습", "모의고사/문제집 독해 및 문법 풀이", "어휘장 누적 암기 및 서술형 영작 연습"],
    "과학": ["교과서 정독 및 나만의 개념 노트 작성", "단원별 기본~응용 문제집 풀이", "오답 원인 분석 및 고난도 자료 해석"]
}

# ---------------------------------------------------------
# 3-(2). 함수 (def) & 3-(3). 조건문 (if-elif-else)
# ---------------------------------------------------------
def recommend_plan(subject, hours, days_left):
    # 시험 남은 일수에 따른 조건 분기 (3일 이하 vs 4일 이상)
    if days_left <= 3:
        status_msg = f"⚠️ 시험이 {days_left}일 남았습니다! 시간이 부족하므로 **핵심 요약 및 기출/오답 위주 전략**을 추천합니다."
        steps = short_term_steps
        methods = short_term_methods[subject]
        # 단기 전략 시간 배분 비율 (핵심 30% : 실전 50% : 점검 20%)
        ratios = [0.3, 0.5, 0.2]
        is_urgent = True
    else:
        status_msg = f"✅ 시험까지 {days_left}일 남았습니다! 시간이 충분하므로 **개념 정리부터 심화까지 탄탄한 정석 전략**을 추천합니다."
        steps = long_term_steps
        methods = long_term_methods[subject]
        # 장기 전략 시간 배분 비율 (개념 40% : 유형 40% : 심화/오답 20%)
        ratios = [0.4, 0.4, 0.2]
        is_urgent = False

    # 과목별 추가 가중치 조건 (수학/과학은 문제풀이 비중을 조금 더 높임)
    if subject in ["수학", "과학"] and not is_urgent:
        ratios = [0.3, 0.5, 0.2]

    # 3-(4). 반복문 (for)을 이용해 표(Table)에 들어갈 데이터 리스트 생성
    plan_data = []
    for i in range(len(steps)):
        allocated_time = round(hours * ratios[i], 1)  # 소수점 첫째 자리까지 계산
        plan_data.append({
            "추천 공부법 단계": steps[i],
            "추천 활동 내용": methods[i],
            "배분 시간": f"{allocated_time} 시간"
        })

    return status_msg, plan_data, is_urgent

# ---------------------------------------------------------
# 2. UI 및 기능 레이아웃 (Streamlit 화면 구성)
# ---------------------------------------------------------
st.title("⏰ 시험 D-Day 맞춤형 공부 계획 추천기")
st.write("과목, 하루 공부 시간, 시험까지 남은 일수를 입력하면 최적의 공부법을 만들어 드립니다.")
st.divider()

# 사용자 입력 받기
subject = st.selectbox("(1) 공부할 과목 선택:", ["국어", "수학", "영어", "과학"])
hours = st.slider("(2) 하루 공부 가능 시간 (시간):", min_value=1.0, max_value=12.0, value=4.0, step=0.5)
days_left = st.number_input("(3) 시험까지 남은 일수 (D-Day):", min_value=1, max_value=60, value=3, step=1)

# 버튼 클릭 시 실행
if st.button("맞춤 공부 계획 만들기", type="primary"):
    st.divider()
    st.subheader("📋 나만의 맞춤 학습 처방전")
    
    # 함수 호출
    message, plan_list, is_urgent = recommend_plan(subject, hours, days_left)
    
    # 결과 1: 텍스트 메시지 출력 (긴급 여부에 따라 박스 색상 다르게 표시)
    if is_urgent:
        st.warning(message)
    else:
        st.success(message)
        
    # 결과 2: 강조 수치 (Metric) 출력
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="오늘의 집중 목표 시간", value=f"{hours} 시간")
    with col2:
        st.metric(label="시험까지 남은 기간", value=f"D-{days_left}")
        
    # 결과 3: 테이블/표 (DataFrame) 출력
    st.write(f"### 📌 [{subject}] 추천 학습 루틴")
    df = pd.DataFrame(plan_list)
    st.table(df)
