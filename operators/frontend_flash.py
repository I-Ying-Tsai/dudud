# academic_decompiler/operators/frontend_flash.py
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from config import config
from core.schemas import AcademicIR

def is_api_overload_error(exception) -> bool:
    err_str = str(exception)
    return "503" in err_str or "429" in err_str or "experiencing high demand" in err_str

class FrontendAnalyzer:
    @classmethod
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception(is_api_overload_error),
        reraise=True,
        before_sleep=lambda retry_state: print(f"  │  [API Notice] Frontend (503/429) high load. Retrying backoff #{retry_state.attempt_number}...")
    )
    def analyze_pdf(cls, client: genai.Client, pdf_bytes: bytes) -> AcademicIR:
        prompt = """
        Analyze the uploaded academic publication PDF and extract its core mathematical formulations. 
        You must isolate the fundamental algebraic operators and fully serialize the tokens, 
        semantic descriptions, and free-text mathematical shape configurations of all input and output tensors.
        Ensure complete mapping of the algorithmic flow and strictly follow the attached JSON schema.

        CRITICAL - MATHEMATICAL DOMAIN & VALUE CONSTRAINT PROPAGATION:
        You must actively conduct semantic analysis on the text surrounding each variable or formula.
        - If the paper text implies or states that a variable/tensor represents a probability vector, density distribution, fraction, or allocation weights that must normalize, you MUST set `constraints.domain_type` to "probability_simplex" and `constraints.sum_to_one` to true.
        - If a variable is strictly required to be non-negative or non-zero due to operational singularities (e.g., inside logs, square roots, or divisions), explicitly assign `domain_type` as "strictly_positive".
        - If a parameter is a scaling coefficient bounded within a real interval (e.g., between 0 and 1), set `domain_type` to "bounded_0_1".
        - For standard unconstrained hidden neural representations, set `domain_type` to "general".

        MATHEMATICAL SYMMETRY GUARD:
        When capturing sequential state transition systems, check algebraic symmetry. Do not introduce hallucinated asymmetric coefficients or variables that break the structural harmony outlined in the paper.
        """
        
        response = client.models.generate_content(
            model=config.frontend_model,
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AcademicIR,
                temperature=0.1
            )
        )
        return AcademicIR.model_validate_json(response.text)