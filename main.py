"""FastAPI application for calculating CHA₂DS₂-VASc score for atrial fibrillation stroke risk."""
from typing import Literal, Annotated

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="CHA₂DS₂-VASc AFSR Score Tool",
    description="API for calculating stroke risk for patients with atrial fibrillation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChadsVascFormInput(BaseModel):
    """Form-based input schema for calculating CHA₂DS₂-VASc score."""

    age: int = Field(
        title="Age",
        ge=1,
        le=150,
        examples=[25],
        description="Enter your age. Must be a value between 1 and 150.",
    )
    biological_sex: Literal["male", "female", "intersex"] = Field(
        title="Biological Sex",
        examples=["male"],
        description="Select your biological sex.",
    )
    congestive_heart_failure: bool = Field(
        title="Congestive Heart Failure",
        examples=[True],
        default=False,
        description="Do you have a history of congestive heart failure?",
    )
    hypertension: bool = Field(
        title="Hypertension",
        examples=[True],
        default=False,
        description="Do you have hypertension?",
    )
    stroke_tia: bool = Field(
        title="Stroke / TIA",
        examples=[True],
        default=False,
        description="Have you experienced a stroke or TIA?",
    )
    vascular_disease: bool = Field(
        title="Vascular Disease",
        examples=[True],
        default=False,
        description="Do you have vascular disease?",
    )
    diabetes: bool = Field(
        title="Diabetes",
        examples=[True],
        default=False,
        description="Do you have diabetes?",
    )


class ChadsVascFormOutput(BaseModel):
    """Form-based output schema for CHA₂DS₂-VASc score."""

    score: int = Field(
        title="CHA₂DS₂-VASc Score",
        examples=[1],
        description="Your calculated CHA₂DS₂-VASc score for atrial fibrillation stroke risk.",
        format="display",
    )


@app.post(
    "/calculate",
    description="Calculate CHA₂DS₂-VASc score for atrial fibrillation stroke risk.",
    response_model=ChadsVascFormOutput,
)
async def calculate_cha2ds2_vasc(data: Annotated[ChadsVascFormInput, Form()],) -> ChadsVascFormOutput:
    """Calculate CHA₂DS₂-VASc score for atrial fibrillation stroke risk.

    Args:
        data (ChadsVascFormInput): The input data for calculating the CHA₂DS₂-VASc score.

    Returns:
        The calculated CHA₂DS₂-VASc score.

    """
    if data.age >= 75:
        age_points = 2
    elif 65 <= data.age < 75:
        age_points = 1
    else:
        age_points = 0

    # Calculate the total CHA₂DS₂-VASc score
    score = (
        age_points +
        (1 if data.biological_sex == "female" else 0) +
        (1 if data.congestive_heart_failure else 0) +
        (1 if data.hypertension else 0) +
        (2 if data.stroke_tia else 0) +
        (1 if data.vascular_disease else 0) +
        (1 if data.diabetes else 0)
    )
    return ChadsVascFormOutput(score=score)
