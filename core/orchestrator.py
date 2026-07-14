# academic_decompiler/core/orchestrator.py
import os
from typing import Optional
from google import genai
from config import config
from core.schemas import AcademicIR
from sandbox.runtime import SandboxRuntime
from operators.frontend_flash import FrontendAnalyzer
from operators.middleend_pro import MiddleEndSynthesizer
from exporters.code_exporter import CodeExporter
from exporters.formula_pdf import FormulaPDFExporter
from exporters.parameter_pdf import ParameterPDFExporter

class AcademicDecompilerOrchestrator:
    def __init__(self):
        self.max_retries = config.max_self_healing_retries
        self.sandbox = SandboxRuntime()
        self.client = genai.Client()

    def run_pipeline(self, pdf_path: str):
        print('=' * 75)
        print(f"LAUNCHING COMPILER ARCHITECTURE: DECOMPILING ACADEMIC CORE [{pdf_path}]")
        print('=' * 75)

        if not os.path.exists(pdf_path):
            print(f" [FATAL] Target file not found: {pdf_path}")
            return
            
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        # -----------------------------------------------------------------
        # Stage 1: Frontend Dynamic Syntactic Parsing
        # -----------------------------------------------------------------
        ir_data = self._execute_frontend(pdf_bytes)
        if not ir_data:
            print(" [FATAL] Frontend structural contract deployment failed. Pipeline halted.")
            return
            
        print(f" ├─ [FRONTEND TEST PASSED]")
        print(f" │  ├── Paper Title: {ir_data.paper_title}")
        print(f" │  └── Extracted Operators Count: {len(ir_data.core_formulas)}")

        # -----------------------------------------------------------------
        # Stage 2: Middle-End JIT Verification & Self-Healing Optimization Loop
        # -----------------------------------------------------------------
        verified_code = self._execute_middleend_loop(ir_data)
        if not verified_code:
            print(" [FATAL] Middle-End self-healing loop failed to align shapes. Pipeline melted.")
            return

        # -----------------------------------------------------------------
        # Stage 3 Placeholder (留待後續打通 Exporters)
        # -----------------------------------------------------------------
        self._execute_exporters(ir_data, verified_code)
        print('=' * 75)
        print("[Status] Pipeline successfully completed with zero downstream leakage.")
        print('=' * 75)

    def _execute_frontend(self, pdf_bytes: bytes) -> Optional[AcademicIR]:
        print(" ├─ [Step Flow] Triggering Frontend Analyzer Operators...")
        try:
            return FrontendAnalyzer.analyze_pdf(self.client, pdf_bytes)
        except Exception as e:
            print(f" │  [Error] Frontend operator failed: {e}")
            return None

    def _execute_middleend_loop(self, ir_data: AcademicIR) -> Optional[str]:
        print(" ├─ [Step Flow] Spawning Middle-End JIT Execution Sandbox...")
        retry_count = 0
        feedback_msg = None
        verified_code = None

        while retry_count <= self.max_retries:
            try:
                code_candidate = MiddleEndSynthesizer.synthesize_code(
                    self.client, ir_data, feedback_loop_msg=feedback_msg
                )
            except Exception as e:
                print(f" │  [ERROR] Middle-End Code Synthesis Failed: {e}")
                return None
            
            # 將合成代碼丟進 Subprocess 沙盒中執行
            success, execution_log = self.sandbox.execute_candidate(code_candidate)
            
            if success:
                print(f" ├─ [SUCCESS] JIT sandbox validation cleared at attempt #{retry_count}! Exit Code 0.")
                snippet = "\n".join(execution_log.strip().splitlines()[-5:])
                print(f" │  [Sandbox Trace Snippet] >>>\n" + "\n".join([f" │  {line}" for line in snippet.splitlines()]))
                verified_code = code_candidate
                break
            else:
                retry_count += 1
                print(f" ├─ [BREAKDOWN] Formal validation step #{retry_count-1} failed. Trapped physical runtime fault.")
                print(' │  [Cleaned Stack Compiler Trace Logs] >>>')
                for line in execution_log.strip().splitlines():
                    print(f" │  {line}")
                
                if retry_count > self.max_retries:
                    print(f" └─ [FATAL] Self-healing circuit broken. Retries exhausted ({self.max_retries}).")
                    return None
                
                feedback_msg = execution_log

        return verified_code

    def _execute_exporters(self, ir_data: AcademicIR, verified_code: str):
        print(" ├─ [Step Flow] Sandboxing cleared. Deploying Parallel Exporter Pipeline...")
        
        try:
            mvi_path = CodeExporter.export_mvi(ir_data, verified_code)
            print(f" │  ├── [Artifact 1] MVI Source Code saved to: {mvi_path}")
        except Exception as e:
            print(f" │  ├── [Error] Failed to export MVI code: {e}")
            
        try:
            topo_pdf_path = FormulaPDFExporter.export_topology(self.client, ir_data, verified_code)
            print(f" │  ├── [Artifact 2] Dataflow Topology PDF saved to: {topo_pdf_path}")
        except Exception as e:
            print(f" │  ├── [Error] Failed to compile Dataflow Topology: {e}")
        
        try:
            spec_pdf_path = ParameterPDFExporter.export_specifications(self.client, ir_data, verified_code)
            print(f" │  └── [Artifact 3] Parameter Specification PDF saved to: {spec_pdf_path}")
        except Exception as e:
            print(f" │  └── [Error] Failed to compile Parameter Specification: {e}")