from stock_predictor.user import models


def get_current_user() -> models.User:
    # TODO: reemplazar con JWT real en auth/
    return models.User(id=1, username="test", email="test@test.com", is_active=True)
