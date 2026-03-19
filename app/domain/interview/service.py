import uuid
from datetime import datetime

from app.database import get_database
from app.domain.interview.models import InterviewDocument, Question
from app.domain.interview.prompt import build_system_prompt, get_first_question_prompt


from app.domain.interview.schema import (
    AnswerRequest,
    AnswerResponse,
    InterviewStartRequest,
    InterviewStartResponse,
)
from app.services.gemini import get_model


async def start_interview(request: InterviewStartRequest) -> InterviewStartResponse:
    """면접 세션을 생성하고 첫 질문을 반환합니다."""
    # TODO: Gemini API 호출하여 첫 질문 생성

    # 1. 시스템 프롬프트 생성
    system_prompt = build_system_prompt(
        job_role=request.job_role,
        tech_stack=request.tech_stack,
        experience_years=request.experience_years,
    )

    # 2. Gemini API 호출 → 첫 질문 생성
    model = get_model()

    chat = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
    response = chat.send_message(get_first_question_prompt())
    first_question = response.text.strip()

    # 3. MongoDB에 세션 저장
    session_id = str(uuid.uuid4())
    now = datetime.now()

    document = InterviewDocument(
        user_id="anonymous",          # 추후 인증 붙이면 교체
        position=request.job_role,
        tech_stack=request.tech_stack,
        career_years=request.experience_years,
        questions=[
            Question(
                question_number=1,
                question_content=first_question,
                category="기술",
                expected_duration_seconds=120,
                created_at=now,
                model_answer="",      # 추후 Gemini로 모범답안 생성 가능
                question_keywords=[],
            )
        ],
        status="in_progress",
        created_at=now,
    )

    db = get_database()
    await db["interviews"].insert_one(
        {**document.model_dump(), "_id": session_id}
    )

    # 4. 응답 반환
    return InterviewStartResponse(
        session_id=session_id,
        question=first_question,
    )
    # TODO: 세션 정보를 MongoDB에 저장
    #raise NotImplementedError


async def submit_answer(request: AnswerRequest) -> AnswerResponse:
    """답변을 분석하고 꼬리 질문을 생성합니다."""
    # TODO: 세션에서 대화 이력 조회
    # TODO: Gemini API 호출하여 꼬리 질문 생성
    # TODO: 답변 및 태도 점수를 MongoDB에 저장
    raise NotImplementedError
