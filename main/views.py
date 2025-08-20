from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from sqlmodel import Session

from google import genai
from google.genai import types

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from ..database import get_db, create_db_and_tables
from .. import models
from ..auth.views import get_current_user
from models import User


load_dotenv()
FastAPI()


router = APIRouter(prefix="/main", tags=["Main App"])

class Input_setting(BaseModel):
    api_key: str
    model: str
    input_text: str

@router.post('/api_storage/', status_code=201)
async def api_storage(input_data: Input_setting, db: Session = Depends(get_current_user)):
    db_user = User(api_key=input_data.api_key)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error has occured")
    return db_user

def handle_input(GEMINI_API_KEY: str, model: str, input: str):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        class requirements(BaseModel):
            score: float = Field(description="The overall score of the essay")
            TR_score : float = Field(description="The score of TR part")
            LR_score : float = Field(description="The score of LR part")
            CC_score : float = Field(description="The score of CC part")
            GRA_score : float = Field(description="The score of GRA part")
        
        generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1,
        ),
        media_resolution="MEDIA_RESOLUTION_MEDIUM",
        response_mime_type="application/json",
        response_schema=requirements,
        system_instruction="""You are an IELTS examiner. I will submit my essay, and you will give it a score and briefly point out any issues."""
        )

        response = client.models.generate_content(
        model=model, 
        contents=input,
        config=generate_content_config
        )

        if response.text:
            parsed_response = requirements.model_validate_json(response.text)
            output = {f"Overall_score: {parsed_response.score}, TR: {parsed_response.TR_score}, LR: {parsed_response.LR_score}, CC:{parsed_response.CC_score}, GRA:{parsed_response.GRA_score}"}
            return output
        else:
            print(response)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Model error")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error occured")

