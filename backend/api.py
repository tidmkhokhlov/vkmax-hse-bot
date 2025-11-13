from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gigachat_answer import get_answer

app = FastAPI()


class QuestionRequest(BaseModel):
  question: str


class AnswerResponse(BaseModel):
  answer: str
  status: str


@app.get("/")
async def root():
  return {"message": "HSE Chat Bot API is running"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
  try:
    response = get_answer(request.question)

    answer_text = response.json()['choices'][0]['message']['content']

    return AnswerResponse(
      answer=answer_text,
      status="success"
    )

  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail=f"Error processing question: {str(e)}"
    )


@app.get("/health")
async def health_check():
  return {"status": "healthy"}