import streamlit as st
from together import Together
import time
import os

# 페이지 설정
st.set_page_config(
    page_title="🤖 Together AI 챗봇",
    page_icon="",
    layout="wide"
)

# 제목과 설명
st.title("🤖 Together AI 챗봇")
st.markdown("---")
st.markdown("**Together AI와 자유롭게 대화해보세요!**")

# 사이드바 - 설정
st.sidebar.header("⚙️ 설정")

# API 키 입력 (환경변수에서 먼저 확인)
default_api_key = os.getenv("TOGETHER_API_KEY", "")
api_key = st.sidebar.text_input(
    "🔑 Together AI API 키",
    value=default_api_key,
    type="password",
    help="https://together.ai/ 에서 API 키를 발급받으세요"
)

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

# 모델 초기화 (세션 상태에 저장)
@st.cache_resource
def load_model(api_key, model_name):
    """AI 모델을 로드합니다."""
    try:
        # Together 라이브러리 올바른 초기화 방식
        client = Together()
        client.api_key = api_key
        return client
    except Exception as e:
        st.error(f"모델 로딩 오류: {e}")
        return None

# API 키가 입력되었을 때만 모델 로드
if api_key:
    with st.spinner("🤖 AI 모델을 불러오는 중..."):
        client = load_model(api_key, model_option)
    
    if client is None:
        st.error("❌ API 키가 올바르지 않습니다. 다시 확인해주세요.")
        st.stop()
else:
    st.warning("⚠️ API 키를 입력해주세요.")
    st.stop()

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

    # AI 응답 생성 - 수정된 부분
    with st.chat_message("assistant"):
        with st.spinner("🤔 AI가 생각하는 중..."):
            try:
                # Together 라이브러리 올바른 API 사용법
                response = client.complete(
                    model=model_option,
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1.1
                )
                
                answer = response['output']['choices'][0]['text']
                st.markdown(answer)
                
                # AI 메시지 추가
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_msg = f"❌ 오류가 발생했습니다: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 사이드바 - 추가 기능
st.sidebar.markdown("---")
st.sidebar.header("️ 도구")

# 대화 초기화 버튼
if st.sidebar.button("🗑️ 대화 초기화"):
    st.session_state.messages = []
    st.rerun()

# 대화 내보내기
if st.sidebar.button("📥 대화 내보내기"):
    if st.session_state.messages:
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

# 정보 표시
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 정보")
st.sidebar.markdown(f"**현재 모델:** {model_option}")
st.sidebar.markdown(f"**대화 수:** {len(st.session_state.messages) // 2}")

# 하단 정보
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p> <strong>팁:</strong> 질문을 구체적으로 하면 더 정확한 답변을 받을 수 있어요!</p>
    <p> 첫 응답은 시간이 걸릴 수 있어요. 기다려주세요!</p>
    <p>🌐 <strong>한국어:</strong> exaone 모델, <strong>영어:</strong> llama 모델 추천</p>
</div>
""", unsafe_allow_html=True)
