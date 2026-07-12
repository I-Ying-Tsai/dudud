# academic_decompiler/core/schemas.py
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ValueConstraint(BaseModel):
    # 數值定義域型態：一般、機率單體（相加為1）、嚴格正數、有界浮點數等
    domain_type: Literal["general", "probability_simplex", "strictly_positive", "bounded_0_1", "orthogonal"] = Field(
        default="general", 
        description="The mathematical domain type derived from paper text context."
    )
    lower_bound: Optional[float] = Field(None, description="Minimum possible scalar value if bounded")
    upper_bound: Optional[float] = Field(None, description="Maximum possible scalar value if bounded")
    sum_to_one: bool = Field(False, description="True if elements across the specified axis must sum to 1.0")

class TensorDeclaration(BaseModel):
    symbol: str = Field(..., description="Tensor token symbol, e.g., 'X', 'W_q', 'U_t'")
    semantic_name: str = Field(..., description="Physical or semantic description of the tensor's role")
    shape_expression: str = Field(..., description="Free-text dimensional declaration, e.g., 'Number of Nodes x Hidden Dim'")
    constraints: ValueConstraint = Field(
        default_factory=ValueConstraint,
        description="Axiomatic mathematical constraints for safe data generation."
    )

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