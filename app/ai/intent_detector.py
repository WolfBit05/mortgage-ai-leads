import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


load_dotenv()


class IntentClassification(BaseModel):
    type: str
    confidence: float = Field(ge=0.0, le=1.0)


class IntentResult(BaseModel):
    primary_intent: IntentClassification
    secondary_intent: IntentClassification | None = None
    signals: list[str] = Field(default_factory=list)
    summary: str


class IntentDetector:

    ALLOWED_INTENTS = {
        "first_time_home_buyer",
        "home_buyer",
        "refinance",
        "mortgage_query",
    }

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def detect(self, title: str, content: str) -> IntentResult:

        prompt = f"""
You are a mortgage lead-intelligence classifier.

Analyze the following Reddit discussion and determine the author's
most relevant mortgage/home-buying intent.

TITLE:
{title}

POST CONTENT:
{content}

Allowed intent categories:

1. first_time_home_buyer
   The author is planning, preparing, or actively trying to purchase
   their first home.

2. home_buyer
   The author is planning, preparing, or actively trying to purchase
   a home, but there is no clear evidence that this is their first home.

3. refinance
   The author already has a mortgage/home loan and is considering
   refinancing, changing their mortgage, lowering their rate/payment,
   or evaluating whether refinancing makes sense.

4. mortgage_query
   The discussion is genuinely mortgage-related, but there is not
   enough evidence of an active home purchase or refinance intent.

Classification rules:

- Specific personal intent takes priority over a generic mortgage question.
- If the author clearly identifies themselves as a first-time buyer,
  prefer first_time_home_buyer over home_buyer.
- Do not classify someone as a home buyer merely because they discuss
  homeownership.
- Do not classify someone as a refinance prospect unless there is
  evidence of an existing mortgage or refinancing context.
- A general educational mortgage question should be mortgage_query.
- Consider the entire context of the post rather than isolated keywords.
- Confidence must represent how strongly the post supports the intent.
- A secondary intent should only be returned when another allowed
  intent is genuinely meaningful in the context.
- If there is no meaningful secondary intent, return null.
- Provide concise signals explaining the classification.
- Provide a short summary of the author's apparent intent.

- Do NOT classify someone as first_time_home_buyer merely because
  the discussion appears in a first-time-home-buyer subreddit.
- first_time_home_buyer requires evidence that the author has never
  owned a home before, explicitly or through clear contextual evidence.
- If the author is clearly considering purchasing a home but there is
  no evidence about whether they have owned a home before, use
  home_buyer instead.

Use subreddit/community context as supporting evidence, but never treat it alone as conclusive proof of first-time status. When first-time status cannot be established, prefer home_buyer with an appropriately lower confidence rather than inventing certainty.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=IntentResult,
                temperature=0,
            ),
        )

        result = IntentResult.model_validate_json(response.text)

        self._validate_intents(result)

        return result

    def _validate_intents(self, result: IntentResult):

        if result.primary_intent.type not in self.ALLOWED_INTENTS:
            raise ValueError(
                f"Invalid primary intent: {result.primary_intent.type}"
            )

        if (
            result.secondary_intent
            and result.secondary_intent.type not in self.ALLOWED_INTENTS
        ):
            raise ValueError(
                f"Invalid secondary intent: "
                f"{result.secondary_intent.type}"
            )