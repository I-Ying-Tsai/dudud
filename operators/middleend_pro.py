# academic_decompiler/operators/middleend_pro.py
from typing import Optional
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from config import config
from core.schemas import AcademicIR

def is_api_overload_error(exception) -> bool:
    err_str = str(exception)
    return "503" in err_str or "429" in err_str or "experiencing high demand" in err_str

class MiddleEndSynthesizer:
    @classmethod
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception(is_api_overload_error),
        reraise=True,
        before_sleep=lambda rs: print(f"  │  [API Notice] Middle-End (503/429) hit high load. Retrying backoff #{rs.attempt_number}...")
    )
    def synthesize_code(cls, client: genai.Client, ir_data: AcademicIR, feedback_loop_msg: Optional[str] = None) -> str:
        ir_context = ir_data.model_dump_json(indent=2)
        
        base_prompt = f"""
        You are an expert applied mathematician and low-level high-performance computing (HPC) engineering kernel optimizer.
        Based on the structured academic Intermediate Representation (IR) JSON metadata provided below, synthesize a production-grade, highly-readable standalone Python function that implements the core formulas.

        [Academic IR Metadata Context]
        {ir_context}

        Rigid Requirements:
        1. Dependency Restriction: ONLY use 'numpy' and 'math'. No external frameworks (e.g., torch, scipy) are allowed.
        2. Main Block Interface: MUST include `if __name__ == '__main__':` execution boundary.
        3. Symbolic & Mathematical Integrity: 
           - Distinguish closely related symbols (e.g., 'alpha' vs 'a'). 
           - Maintain mathematical symmetry: if the paper defines symmetric parallel updates (e.g., Support and Denial branches), do NOT introduce hallucinated asymmetric coefficients (like an extraneous beta) into one branch.
        4. Mandatory JIT Test Suite Specification:
           Your test block MUST explicitly evaluate and assert the following adversarial operational conditions:
           - TENSOR CONCATENATION & COMPRESSION: Verify that concatenated representations (e.g., [3H]) are correctly projected back to [H] via linear transformations before element-wise additions.
           - DYNAMIC BOUNDARY & EXTREME TREE DEPTH: Instantiate tests for deep trees (e.g., T=5) AND extreme shallow trees (e.g., T=1). Ensure no IndexOutOfBounds or null reduction errors occur in temporal loops or KL loss summations.
           - BROADCAST IMMUNITY: Ensure node-count scaling (e.g., b_u * u_hat) correctly utilizes NumPy broadcasting without distorting batch or hidden tensor profiles.
        5. Assertions: Explicitly use `assert` to validate matrix shapes and numerical stability (no NaN/Inf).
        6. Output Formatting: Pure executable Python string ONLY. NO Markdown wrappers (like ```python).
        """
        
        contents = [base_prompt]
        
        if feedback_loop_msg:
            print(' │  [Middle-End] Sandboxed runtime failure intercepted! Triggering contextual feedback healing loop...')
            interrupt_prompt = f"""
            [SANDBOX RUNTIME CRASH REPORT]
            Your previous code failed to execute inside the physical python runtime sandbox! 
            Traceback error log:
            {feedback_loop_msg}
            
            Critical Instructions:
            - Analyze exact axis indexing, matrix shape alignments, transpositions, and loop bounds.
            - Debug the faulty logic. Re-synthesize and output the completely corrected, raw, error-free Python implementation. Do NOT wrap code inside Markdown blocks.
            """
            contents.append(interrupt_prompt)
            
        response = client.models.generate_content(
            model=config.middleend_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.1 if not feedback_loop_msg else 0.3
            )
        )
        
        # 穩定清洗 Markdown 標籤
        code = response.text.strip()
        if code.startswith("```python"):
            code = code.split("```python")[1].split("```")[0].strip()
        elif code.startswith("```"):
            code = code.split("```")[1].split("```")[0].strip()
        return code