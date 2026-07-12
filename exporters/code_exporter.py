# academic_decompiler/exporters/code_exporter.py
import os
import re
from datetime import datetime
from config import config
from core.schemas import AcademicIR

class CodeExporter:
    @staticmethod
    def export_mvi(ir_data: AcademicIR, verified_code: str) -> str:
        os.makedirs(config.output_dir, exist_ok=True)
        
        # 清洗論文標題作為檔名 (e.g., "Epidemiology-informed Network" -> "epidemiology_informed_network")
        clean_title = re.sub(r'[^a-zA-Z0-9]+', '_', ir_data.paper_title).strip('_').lower()
        # 截斷過長的檔名
        if len(clean_title) > 50:
            clean_title = clean_title[:50]
            
        filename = f"{clean_title}_mvi.py"
        filepath = os.path.join(config.output_dir, filename)
        
        # 構建專業的工程標頭
        header = f'"""\n'
        header += f'Academic Decompiler - Minimal Viable Implementation (MVI)\n'
        header += f'=========================================================\n'
        header += f'Paper: {ir_data.paper_title}\n'
        header += f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        header += f'Status: [VERIFIED] Passed Subprocess JIT Sandbox\n'
        header += f'"""\n\n'
        
        final_content = header + verified_code
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        return filepath