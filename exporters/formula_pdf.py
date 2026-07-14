# academic_decompiler/exporters/formula_pdf.py
import os
import re
from google import genai
from google.genai import types
from graphviz import Source
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from config import config
from core.schemas import AcademicIR

def is_api_overload_error(exception) -> bool:
    err_str = str(exception)
    return "503" in err_str or "429" in err_str or "experiencing high demand" in err_str

class FormulaPDFExporter:
    @classmethod
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception(is_api_overload_error),
        reraise=True,
        before_sleep=lambda rs: print(f"  │  [API Notice] Backend (503/429) hit high load. Retrying backoff #{rs.attempt_number}...")
    )
    def export_topology(cls, client: genai.Client, ir_data: AcademicIR, verified_code: str) -> str:
        print(' │  [Backend] Compiling generalized causality-correct topology graph with Vertical Bus layout...')
        os.makedirs(config.output_dir, exist_ok=True)
        
        ir_context = ir_data.model_dump_json(indent=2)
        
        prompt = f"""
        You are an elite academic compiler architect and expert typographer.
        
        [Academic IR Context]
        {ir_context}
        
        [Verified NumPy Code]
        {verified_code}

        Task:
        Synthesize a vertically compact, causality-correct Graphviz DOT directed graph (digraph G).

        GENERALIZED CAUSALITY & DEPENDENCY ALGORITHMS (CRITICAL):
        1. STRICT OPERAND TRACING (NO MISSING EDGES):
           You must act as an Abstract Syntax Tree (AST) parser. For EVERY mathematical operation in the verified code (e.g., matrix multiplications, element-wise additions), there MUST exist a directed edge from ALL operands (both the weights/parameters AND the states) into the operation node. Do NOT omit dependency edges for any parameters.
        2. THEORETICAL DECOUPLING:
           Identify pure theoretical background continuous models (e.g., abstract differential equations) and isolate them into a completely disconnected 'cluster_theory'. Do NOT draw dataflow edges from abstract theoretical rates into the discrete algorithmic forward pass.
        3. DYNAMIC ABBREVIATION:
           Dynamically generate collision-resistant uppercase acronyms for all formulas. Node labels MUST only contain the Math Symbol and your auto-generated Acronym. Max 2 lines.

        RIGID LAYOUT & ANTI-BLOAT GEOMETRY (VERTICAL BUS):
        - Declare: size="8.3,11.7!", ratio="fill", margin=0.2, nodesep=0.15, ranksep=0.4, rankdir=TB.
        - VERTICAL PARAMETER BUS TACTIC: To prevent horizontal bloating, you MUST group all independent static parameters (weights, biases, scalars) and force them to stack vertically. Achieve this by connecting them with invisible edges (e.g., Param1 -> Param2 -> Param3 [style=invis]). This forces Graphviz to arrange them in a narrow vertical column, saving immense horizontal A4 space.

        COLOR & EDGE HIERARCHY:
        - Static params: Pastel Yellow. Recurrent States: Pastel Blue. Operations: Pastel Grey (ellipse). Loss/Output: Muted Red.
        - Main Tensor Flow: Bold solid (penwidth=2.5, color="#2A4B7C").
        - Parameter Injections: Thin dashed (penwidth=1.2, color="#7F7F7F").

        Output ONLY raw Graphviz DOT source code starting with "digraph G {{" and ending with "}}". NO markdown. NO splines=curved.
        """
        
        response = client.models.generate_content(
            model=config.backend_model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        dot_source = response.text.strip()
        if dot_source.startswith("```"):
            lines = dot_source.splitlines()
            dot_source = "\n".join([line for line in lines if not line.startswith("```")])
            
        clean_title = re.sub(r'[^a-zA-Z0-9]+', '_', ir_data.paper_title).strip('_').lower()[:50]
        output_path = os.path.join(config.output_dir, f"{clean_title}_topology")
        
        src = Source(dot_source)
        compiled_pdf_path = src.render(filename=output_path, format="pdf", cleanup=True)
        return compiled_pdf_path