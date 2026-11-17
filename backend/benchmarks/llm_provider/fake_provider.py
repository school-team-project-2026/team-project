from app.ai.schemas import PreferenceFeatures


class FakeProvider:
    provider_name = "fake"
    model_name = "fake-model"

    def extract(
        self,
        *,
        name: str,
        category: str,
        comment: str,
    ) -> PreferenceFeatures:
        return PreferenceFeatures(
            attributes=[category],
            appeal_points=[comment],
            desired_experiences=[],
            values=[],
            keywords=[name],
        )
