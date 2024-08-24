from aws_client.artwork_table import ArtWork
from aws_lambda_powertools import Logger
from pynamodb.pagination import ResultIterator

logger = Logger(child=True)


def get_artworks() -> list[ArtWork]:
    """作品一覧取得

    Returns:
        list[ArtWork]: 作品一覧
    """
    # TODO: ページネーションの考慮
    itr_artworks: ResultIterator[ArtWork] = ArtWork.scan_artworks()
    articles: list[ArtWork] = [i for i in itr_artworks]
    return articles
