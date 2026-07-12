# academic_decompiler/core/schemas.py
from typing import List
from pydantic import BaseModel, Field

class TensorDeclaration(BaseModel):
    symbol: str = Field(..., description="Tensor token symbol, e.g., 'X', 'W_q', 'U_t'")
    semantic_name: str = Field(..., description="Physical or semantic description of the tensor's role")
    shape_expression: str = Field(..., description="Free-text dimensional declaration, e.g., 'Number of Nodes x Hidden Dim'")

class FormulaNode(BaseModel):
    node_id: str = Field(..., description="Unique algebraic operator identifier, e.g., 'eq1', 'eq2'")
    name: str = Field(..., description="Academic name of the mathematical process")
    latex_code: str = Field(..., description="Pure LaTeX mathematical expression string extracted from the paper")
    inputs: List[TensorDeclaration] = Field(default_factory=list, description="List of operand input tensors")
    outputs: List[TensorDeclaration] = Field(default_factory=list, description="List of resultant output tensors")

class AcademicIR(BaseModel):
    paper_title: str = Field(..., description="The verified title of the scanned academic publication")
    core_formulas: List[FormulaNode] = Field(default_factory=list, description="Chronological sequence of foundational math nodes")
    algorithm_pseudocode: str = Field(..., description="High-level algorithmic execution trace or step description")