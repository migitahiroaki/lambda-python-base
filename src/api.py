from typing import Any
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from biz import artwork
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

app = APIGatewayRestResolver()
logger = Logger(child=True)


@app.get("/artworks")
def get_artworks() -> dict[str, Any]:
    # TODO: pydanticなどでレスポンスモデル作成
    return {"artworks": artwork.get_artworks()}


def lambda_handler(event: dict, context: LambdaContext) -> dict[str, Any]:
    return app.resolve(event, context)
