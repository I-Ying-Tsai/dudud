# academic_decompiler/core/orchestrator.py
import os
from typing import Optional
from google import genai
from config import config
from core.schemas import AcademicIR
from sandbox.runtime import SandboxRuntime
from operators.frontend_flash import FrontendAnalyzer

class AcademicDecompilerOrchestrator:
    def __init__(self):
        self.max_retries = config.max_self_healing_retries
        self.sandbox = SandboxRuntime()
        self.client = genai.Client()

    def run_pipeline(self, pdf_path: str):
        print('=' * 75)
        print(f"LAUNCHING COMPILER ARCHITECTURE: DECOMPILING ACADEMIC CORE [{pdf_path}]")
        print('=' * 75)

        # Read binary stream
        if not os.path.exists(pdf_path):
            print(f" [FATAL] Target file not found: {pdf_path}")
            return
            
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        # -----------------------------------------------------------------
        # Stage 1: Frontend Dynamic Syntactic Parsing (真實對接測試點)
        # -----------------------------------------------------------------
        ir_data = self._execute_frontend(pdf_bytes)
        if not ir_data:
            print(" [FATAL] Frontend structural contract deployment failed. Pipeline halted.")
            return
            
        # 測試中斷點：目前先將解析成功的 IR 資料美化列印出來
        print(f" ├─ [FRONTEND TEST PASSED]")
        print(f" │  ├── Paper Title: {ir_data.paper_title}")
        print(f" │  └── Extracted Operators Count: {len(ir_data.core_formulas)}")
        for node in ir_data.core_formulas:
            print(f" │      ├── [{node.node_id}] {node.name}")
            print(f" │      └── LaTeX: {node.latex_code}")

        # -----------------------------------------------------------------
        # Stage 2 & 3 Placeholder (留待後續打通)
        # -----------------------------------------------------------------
        print(" ├─ [Pipeline Link] Middle-End & Exporters are bypassed during this test segment.")

    def _execute_frontend(self, pdf_bytes: bytes) -> Optional[AcademicIR]:
        print(" ├─ [Step Flow] Triggering Frontend Analyzer Operators...")
        try:
            return FrontendAnalyzer.analyze_pdf(self.client, pdf_bytes)
        except Exception as e:
            print(f" │  [Error] Frontend operator failed: {e}")
            return None