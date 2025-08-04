import streamlit as st
import time
import os

# 페이지 설정
st.set_page_config(
    page_title="🤖 Together AI 챗봇",
    page_icon="🤖",
    layout="wide"
)

# Together 라이브러리 동적 import 및 버전 확인
@st.cache_resource
def setup_together_client():
    """Together 라이브러리를 안전하게 import하고 설정합니다."""
    try:
        # 동적 import로 버전 호환성 확인
        import together
        
        # 버전 정보 표시
        version = getattr(together, '__version__', 'Unknown')
        st.sidebar.success(f"✅ Together 버전: {version}")
        
        return together
    except ImportError as e:
        st.error(f"❌ Together 라이브러리를 불러올 수 없습니다: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ 예상치 못한 오류: {e}")
        st.stop()

# Together 라이브러리 설정
together_lib = setup_together_client()

# 제목과 설명
st.title("🤖 Together AI 챗봇")
st.markdown("---")
st.markdown("**Together AI와 자유롭게 대화해보세요!**")

# 사이드바 - 설정
st.sidebar.header("⚙️ 설정")

# API 키 입력
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

# 안전한 클라이언트 초기화 함수
def create_together_client(api_key):
    """다양한 방식으로 Together 클라이언트 초기화를 시도합니다."""
    if not api_key or len(api_key.strip()) == 0:
        return None, "API 키가 입력되지 않았습니다."
    
    # 여러 방식으로 초기화 시도
    initialization_methods = [
        # 방법 1: 키워드 인자 방식 (최신)
        lambda: together_lib.Together(api_key=api_key),
        # 방법 2: 위치 인자 방식 (구버전 호환)
        lambda: together_lib.Together(api_key),
        # 방법 3: 환경변수 설정 후 초기화
        lambda: _init_with_env_var(api_key),
    ]
    
    for i, method in enumerate(initialization_methods, 1):
        try:
            st.sidebar.info(f"🔄 초기화 방법 {i} 시도 중...")
            client = method()
            st.sidebar.success(f"✅ 방법 {i}로 성공!")
            return client, "성공"
        except Exception as e:
            st.sidebar.warning(f"⚠️ 방법 {i} 실패: {str(e)[:50]}...")
            continue
    
    return None, "모든 초기화 방법이 실패했습니다."

def _init_with_env_var(api_key):
    """환경변수를 설정한 후 초기화하는 방법"""
    os.environ['TOGETHER_API_KEY'] = api_key
    return together_lib.Together()

# 클라이언트 초기화
client = None
if api_key:
    with st.spinner("🤖 AI 모델 초기화 중..."):
        client, init_result = create_together_client(api_key)
    
    if client is None:
        st.error(f"❌ {init_result}")
        st.info("💡 **해결 방법:**")
        st.info("1. API 키를 다시 확인해보세요")
        st.info("2. 잠시 후 페이지를 새로고침해보세요")
        st.info("3. Streamlit Cloud의 캐시를 초기화해보세요")
        st.stop()
    else:
        st.success("✅ AI 모델이 성공적으로 로드되었습니다!")
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

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🤔 AI가 생각하는 중..."):
            try:
                # API 호출을 위한 메시지 구성
                api_messages = [{"role": "user", "content": prompt}]
                
                # Together AI API 호출
                response = client.chat.completions.create(
                    model=model_option,
                    messages=api_messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                st.markdown(answer)
                
                # AI 메시지 추가
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_msg = f"❌ 오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                
                # 디버깅 정보
                with st.expander("🔍 디버그 정보"):
                    st.code(f"오류 타입: {type(e).__name__}")
                    st.code(f"오류 내용: {str(e)}")
                    st.code(f"사용 모델: {model_option}")

# 사이드바 - 추가 기능
st.sidebar.markdown("---")
st.sidebar.header("🛠️ 도구")

# 대화 초기화 버튼
if st.sidebar.button("🗑️ 대화 초기화"):
    st.session_state.messages = []
    st.rerun()

# 캐시 초기화 버튼 (Streamlit Cloud 문제 해결용)
if st.sidebar.button("🔄 캐시 초기화"):
    st.cache_resource.clear()
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

# 시스템 정보
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 시스템 정보")
st.sidebar.markdown(f"**Python 버전:** {st.__version__}")
st.sidebar.markdown(f"**현재 모델:** {model_option}")
st.sidebar.markdown(f"**대화 수:** {len(st.session_state.messages) // 2}")

# 하단 정보
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <strong>Streamlit Cloud 팁:</strong> 문제가 지속되면 캐시 초기화 버튼을 눌러보세요!</p>
    <p>🌐 <strong>한국어:</strong> exaone 모델, <strong>영어:</strong> llama 모델 추천</p>
</div>
""", unsafe_allow_html=True)
