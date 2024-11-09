import logging
import os
from typing import TypedDict, List

logger = logging.getLogger(__name__)

LOG_LEVEL = logging.getLevelNamesMapping().get(os.getenv("LOG_LEVEL"), logging.INFO)


class ModelData(TypedDict):
    lang: str
    model: str


def get_models_data() -> List[ModelData]:
    models_path = os.getenv("MODELS_PATH")
    env_models_data = os.getenv("MODELS", None)
    if not env_models_data:
        raise Exception("Models data is not provided")

    res: List[ModelData] = list()

    for m in env_models_data.split("|"):
        try:
            [lang, model] = m.split(":")

            if not (lang and model):
                logger.warning("model and lang can't be empty")
                continue

        except ValueError as e:
            logger.warning(f"Invalid model data string: {str(e)}")
            continue

        res.append({"lang": lang, "model": os.path.join(models_path, model)})

    if len(res) == 0:
        raise Exception("failed to load models data")

    return res
