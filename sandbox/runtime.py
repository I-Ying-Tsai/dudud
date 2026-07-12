import os
import sys
import subprocess
from config import config
from sandbox.verifier import ASTSecurityVerifier

class SandboxRuntime:
    def __init__(self):
        self.timeout = config.sandbox_timeout_seconds
        self.temp_filename = "_sandbox_jit_runtime.py"

    def execute_candidate(self, code_str: str) -> tuple[bool, str]:
        # Step 1: Static AST Firewall Verification
        is_safe, security_msg = ASTSecurityVerifier.verify_code(code_str)
        if not is_safe:
            return False, f"[AST Intercept Block] {security_msg}"

        # Step 2: Write volatile buffer to storage descriptor
        with open(self.temp_filename, 'w', encoding='utf-8') as f:
            f.write(code_str)

        # Step 3: Fork and execute inside clean environment
        try:
            result = subprocess.run(
                [sys.executable, self.temp_filename],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, self._clean_traceback(result.stderr)
        except subprocess.TimeoutExpired:
            return False, f"Execution Timeout: Code logic exceeded max duration limit ({self.timeout}s)."
        except Exception as e:
            return False, f"Sandbox Critical Core Infrastructure Fault: {str(e)}"
        finally:
            if os.path.exists(self.temp_filename):
                os.remove(self.temp_filename)

    def _clean_traceback(self, raw_stderr: str) -> str:
        lines = raw_stderr.splitlines()
        output = []
        keep = False
        for line in lines:
            if 'Traceback' in line or self.temp_filename in line:
                keep = True
            if keep:
                output.append(line.replace(self.temp_filename, 'candidate_kernel.py'))
        return '\n'.join(output) if output else raw_stderr