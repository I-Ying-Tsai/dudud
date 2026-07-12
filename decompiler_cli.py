# decompiler_cli.py
import sys
from core.orchestrator import AcademicDecompilerOrchestrator

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 decompiler_cli.py <path_to_paper.pdf>")
        sys.exit(1)
        
    orchestrator = AcademicDecompilerOrchestrator()
    orchestrator.run_pipeline(sys.argv[1])