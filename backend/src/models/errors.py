from src.utils.result import Result


class EntitiesErrorMessages:
    @staticmethod
    def error_creating_news() -> Result:
        return Result.Error('Error creating news')
