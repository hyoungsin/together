import streamlit as st
import requests
import json
import time

# 페이지 설정
st.set_page_config(
    page_title="🤖 Together AI 챗봇",
    page_icon="🤖",
    layout="wide"
)

# 제목과 설명
st.title("🤖 Together AI 챗봇")
st.markdown("---")
st.markdown("**Together AI와 자유롭게 대화해보세요!**")

# 사이드바 - 설정
st.sidebar.header("⚙️ 설정")

# API 키 입력 (자동입력 제거)
api_key = st.sidebar.text_input(
    "🔑 Together AI API 키",
    value="",  # 빈 값으로 설정
    type="password",
    placeholder="sk-... 형태의 API 키를 입력하세요",
    help="https://together.ai/ 에서 API 키를 발급받으세요"
)

# 보안 안내 메시지
st.sidebar.info("🔒 **보안 팁**: API 키는 절대 공유하지 마세요!")

# 모델 선택
model_option = st.sidebar.selectbox(
    "🤖 AI 모델 선택",
    [
        "lgai/exaone-3-5-32b-instruct",
        "lgai/exaone-deep-32b", 
        "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    ],
    help="사용할 AI 모델을 선택하세요"
)

# 모델 설명
model_descriptions = {
    "lgai/exaone-3-5-32b-instruct": "한국어 특화 32B Instruct 모델",
    "lgai/exaone-deep-32b": "한국어 특화 32B Deep 모델",
    "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free": "영어 특화 70B Turbo Free 모델"
}

st.sidebar.markdown(f"**선택된 모델:** {model_option}")
st.sidebar.markdown(f"*{model_descriptions[model_option]}*")

# Together API 직접 호출 함수
def call_together_api(api_key, model, messages, max_tokens=1000, temperature=0.7):
    """Together API를 직접 호출합니다."""
    
    url = "https://api.together.xyz/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1.1,
        "stop": ["<|eot_id|>", "<|end_of_text|>"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = f"API 오류 (코드: {response.status_code})"
            try:
                error_detail = response.json()
                if 'error' in error_detail:
                    error_msg += f": {error_detail['error'].get('message', '알 수 없는 오류')}"
            except:
                error_msg += f": {response.text}"
            return None, error_msg
            
    except requests.exceptions.Timeout:
        return None, "요청 시간 초과 (60초). 다시 시도해주세요."
    except requests.exceptions.ConnectionError:
        return None, "네트워크 연결 오류. 인터넷 연결을 확인해주세요."
    except Exception as e:
        return None, f"예상치 못한 오류: {str(e)}"

# API 키 검증 및 안내
if not api_key:
    st.warning("⚠️ API 키를 입력해주세요.")
    
    # API 키 발급 안내
    with st.expander("🔑 API 키 발급 방법"):
        st.markdown("""
        **Together AI API 키 발급받기:**
        
        1. 🌐 [Together AI 웹사이트](https://together.ai/) 방문
        2. 🔐 계정 생성 또는 로그인
        3. ⚙️ API 키 섹션으로 이동
        4. ➕ 새 API 키 생성
        5. 📋 생성된 키를 복사해서 왼쪽에 입력
        
        **주의사항:**
        - API 키는 `sk-`로 시작해요
        - 키를 잃어버리면 재발급 받아야 해요
        - 절대 다른 사람과 공유하지 마세요! 🚫
        """)
    st.stop()

# API 키 형식 검증
elif not api_key.startswith('sk-') or len(api_key) < 20:
    st.error("❌ API 키 형식이 올바르지 않습니다. 'sk-'로 시작하는 키를 입력해주세요.")
    st.stop()
else:
    st.success("✅ API 키가 입력되었습니다!")

# 채팅 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🤔 AI가 생각하는 중..."):
            try:
                # API 호출을 위한 메시지 구성 (최근 10개 메시지만)
                recent_messages = st.session_state.messages[-10:]
                
                # Together API 직접 호출
                response_data, error = call_together_api(
                    api_key=api_key,
                    model=model_option,
                    messages=recent_messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                if error:
                    st.error(f"❌ {error}")
                    
                    # 일반적인 해결책 제안
                    with st.expander("💡 해결 방법"):
                        st.markdown("""
                        **가능한 해결책:**
                        1. API 키가 올바른지 확인해보세요
                        2. 계정의 크레딧이 충분한지 확인해보세요  
                        3. 선택한 모델이 사용 가능한지 확인해보세요
                        4. 잠시 후 다시 시도해보세요
                        """)
                    
                elif response_data and 'choices' in response_data:
                    answer = response_data['choices'][0]['message']['content'].strip()
                    
                    if answer:
                        st.markdown(answer)
                        # AI 메시지 추가
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("❌ AI가 빈 응답을 반환했습니다.")
                        
                else:
                    st.error("❌ 예상치 못한 응답 형식입니다.")
                    
            except Exception as e:
                st.error(f"❌ 처리 중 오류가 발생했습니다: {str(e)}")

# 사이드바 - 추가 기능
st.sidebar.markdown("---")
st.sidebar.header("🛠️ 도구")

# 대화 초기화 버튼
if st.sidebar.button("🗑️ 대화 초기화"):
    st.session_state.messages = []
    st.rerun()

# 대화 내보내기
if st.sidebar.button("📥 대화 내보내기") and st.session_state.messages:
    chat_text = ""
    for msg in st.session_state.messages:
        role = "사용자" if msg["role"] == "user" else "AI"
        chat_text += f"**{role}:** {msg['content']}\n\n"
    
    st.sidebar.download_button(
        label="💾 대화 저장",
        data=chat_text,
        file_name=f"together_chat_{time.strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# API 테스트 기능
if st.sidebar.button("🔧 API 연결 테스트"):
    with st.spinner("API 연결을 테스트하는 중..."):
        test_messages = [{"role": "user", "content": "안녕하세요"}]
        response_data, error = call_together_api(
            api_key=api_key,
            model=model_option,
            messages=test_messages,
            max_tokens=10,
            temperature=0.1
        )
        
        if error:
            st.sidebar.error(f"❌ 테스트 실패: {error}")
        else:
            st.sidebar.success("✅ API 연결 성공!")

# 정보 표시
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 정보")
st.sidebar.markdown(f"**현재 모델:** {model_option}")
st.sidebar.markdown(f"**대화 수:** {len(st.session_state.messages) // 2}")

# 보안 안내
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 보안 안내")
st.sidebar.warning("API 키는 세션이 끝나면 자동으로 삭제됩니다.")

# 하단 정보
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔒 <strong>보안:</strong> API 키는 안전하게 관리되며 저장되지 않습니다</p>
    <p>💡 <strong>팁:</strong> 구체적인 질문을 하면 더 정확한 답변을 받을 수 있어요!</p>
    <p>🌐 <strong>한국어:</strong> exaone 모델, <strong>영어:</strong> llama 모델 추천</p>
</div>
""", unsafe_allow_html=True)
