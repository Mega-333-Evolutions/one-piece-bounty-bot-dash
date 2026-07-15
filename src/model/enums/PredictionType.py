from enum import Enum


class PredictionType(Enum):
    """
    Enum class for predictions type
    """
    VERSUS = "Versus"
    PREFERENCE = "Preference"
    EVENT = "Event"


def get_all_prediction_type_names() -> list[str]:
    """
    Get the names of all known prediction types (Versus, Preference, Event).
    Legacy/unknown type values stored on a Prediction (e.g. "User") are intentionally not included here,
    so they never show up as a filter option and can never be matched by a "type in (...)" filter built from this.
    :return: All known prediction type names
    """

    return [prediction_type.value for prediction_type in PredictionType]
