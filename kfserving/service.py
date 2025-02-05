from typing import List

import pydantic
import numpy as np
import bentoml
from bentoml.io import NumpyNdarray, JSON

iris_clf_runner = bentoml.sklearn.get("iris_clf:latest").to_runner()

svc = bentoml.Service("iris_classifier", runners=[iris_clf_runner])

class KFServingInputSchema(pydantic.BaseModel):
    instances: List[List[float]] 

kfserving_input = JSON(
    pydantic_model=KFServingInputSchema,
    validate_json=True,
)

@svc.api(
    input=kfserving_input,
    output=NumpyNdarray(),
    route="v1/models/iris_classifier",
)
def classify(kf_input: KFServingInputSchema) -> np.ndarray:
    instances = np.array(kf_input.instances)
    return iris_clf_runner.predict.run(instances)
