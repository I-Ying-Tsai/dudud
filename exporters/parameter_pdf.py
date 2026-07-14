# academic_decompiler/exporters/parameter_pdf.py
import os
import re
from google import genai
from google.genai import types
from xhtml2pdf import pisa
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from config import config
from core.schemas import AcademicIR

def is_api_overload_error(exception) -> bool:
    err_str = str(exception)
    return "503" in err_str or "429" in err_str or "experiencing high demand" in err_str or "Empty response" in err_str

class ParameterPDFExporter:
    @classmethod
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception(is_api_overload_error),
        reraise=True,
        before_sleep=lambda rs: print(f"  │  [API Notice] Analyzer hit high load or empty response. Retrying backoff #{rs.attempt_number}...")
    )
    def export_specifications(cls, client: genai.Client, ir_data: AcademicIR, verified_code: str) -> str:
        print(' │  [Backend] Executing Static Dimension Constraint Solver & generating specs...')
        os.makedirs(config.output_dir, exist_ok=True)
        
        ir_context = ir_data.model_dump_json(indent=2)
        
        prompt = f"""
        You are an elite academic compiler architect and static type-checker.
        Generate a highly compact, mathematically flawless HTML technical specification.
        
        [Academic IR Context]
        {ir_context}

        [Verified NumPy Code]
        {verified_code}

        GENERALIZED NEURO-SYMBOLIC UNIFICATION ALGORITHM (CRITICAL):
        You must act as a Static Dimension Constraint Solver before generating the specification sheet:
        1. ALGEBRAIC DIMENSION UNIFICATION (ELIMINATE HALLUCINATIONS):
           - Rule: If two tensors undergo element-wise addition (A + B) or concatenation-then-projection back to a base dimension, their shapes MUST be strictly unified to the exact same dimension symbol (e.g., both must be [Hidden Dim]).
           - Execution: NEVER invent arbitrary or non-existent downstream dimensions (like "[Output Dim]") if the mathematical operations in the verified code prove they align with a preexisting feature dimension.
        2. STATISTICAL SIMPLEX TYPING:
           - Rule: Any variable involved in distributional loss functions (e.g., KL Divergence, Cross-Entropy) or outputs of Softmax MUST be explicitly typed and dimensioned as a "Probability Simplex Vector [Num_Classes]". 
           - Execution: Do NOT type them based on spatial/graph domains (like "Number of Nodes") and do NOT declare them as disjoint independent scalars. They are mathematically unified probability vectors.

        RIGID SPACE-SAVING & ULTRA-COMPACT LAYOUT RULES (xhtml2pdf):
        - Your final HTML output MUST fit tightly within 2 to 3 pages maximum.
        - CSS Styling Constraints:
          * @page margins: 0.35in all around.
          * Body: Font-family: Arial, Helvetica; font-size: 8.5pt; line-height: 1.15.
          * Tables: width: 100%; border-collapse: collapse; margin-bottom: 8px; page-break-inside: avoid.
          * Table Padding: Header 4px 6px; Data 3px 5px. Zebra striping.
        
        Required Sections in HTML:
        1. DOCUMENT TITLE.
        2. AUTO-GENERATED ACRONYM DECODER TABLE (Map the dynamically generated Topology acronyms).
        3. RIGID SYMBOL SPECIFICATION SHEET (Columns: Symbol, Semantic Name, True Unified Dimension, Constraints, Mathematical Role). Ensure the Dimension column strictly obeys your Unification Solver results.
        4. ENGINEERING DEEP-DIVES.

        Output raw HTML string starting with "<!DOCTYPE html>" and ending with "</html>". Do NOT wrap in markdown.
        """
        
        response = client.models.generate_content(
            model=config.analyzer_model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        if not response or not response.text:
            raise RuntimeError("Empty response received from API (possible safety filter drop or silent failure). Forcing retry...")
            
        html_content = response.text.strip()
        if html_content.startswith("```"):
            lines = html_content.splitlines()
            html_content = "\n".join([line for line in lines if not line.startswith("```")])
            
        clean_title = re.sub(r'[^a-zA-Z0-9]+', '_', ir_data.paper_title).strip('_').lower()[:50]
        pdf_filename = f"{clean_title}_specifications.pdf"
        pdf_filepath = os.path.join(config.output_dir, pdf_filename)
        
        with open(pdf_filepath, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
            
        if pisa_status.err:
            raise RuntimeError(f"xhtml2pdf failed to render specification report with status: {pisa_status.err}")
            
        return pdf_filepath