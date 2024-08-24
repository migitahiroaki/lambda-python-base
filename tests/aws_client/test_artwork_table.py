from typing import Any, Generator
from aws_client.artwork_table import ArtWork
from moto import mock_aws
import pytest
from pynamodb.pagination import ResultIterator


@pytest.fixture(scope="session", autouse=True)
def mock_dynamodb():
    """DynamoDBをモック化する"""
    mock_aws().start()
    yield
    mock_aws().stop()


@pytest.fixture(scope="module", autouse=True)
def artwork_table():
    """artworkテーブル作成"""
    response = ArtWork.create_table()
    print(response)
    yield
    ArtWork.delete_table()


@pytest.fixture(scope="function")
def artwork_aaa() -> Generator[ArtWork, Any, None]:
    """id=aのartworkレコード作成"""
    artwork: ArtWork = ArtWork(hash_key="aaa", title="title A", body="AAA")
    save_result: dict[str, Any] = artwork.save()
    print(save_result)
    yield artwork
    artwork.delete()


@pytest.fixture(scope="function")
def artwork_bbb() -> Generator[ArtWork, Any, None]:
    """id=aのartworkレコード作成"""
    artwork: ArtWork = ArtWork(hash_key="bbb", title="title B", body="BBB")
    save_result: dict[str, Any] = artwork.save()
    print(save_result)
    yield artwork
    artwork.delete()


@pytest.fixture(scope="function")
def artwork_ccc() -> Generator[ArtWork, Any, None]:
    """id=aのartworkレコード作成"""
    artwork: ArtWork = ArtWork(hash_key="ccc", title="title C", body="CCC")
    save_result: dict[str, Any] = artwork.save()
    print(save_result)
    yield artwork
    artwork.delete()


def test_get_artwork_by_id(artwork_aaa: ArtWork):
    """IDで作品取得"""
    actual = ArtWork.get(hash_key=artwork_aaa.id)
    # オブジェクトとしては別だが、同一のDBデータであることを確認
    assert hash(artwork_aaa) != hash(actual)
    assert artwork_aaa.attribute_values == actual.attribute_values


def test_scan_artworks(
    artwork_aaa: ArtWork, artwork_bbb: ArtWork, artwork_ccc: ArtWork
):
    """作品一覧取得"""
    iterator: ResultIterator[ArtWork] = ArtWork.scan_artworks()

    assert [artwork_aaa.id, artwork_bbb.id, artwork_ccc.id] == [i.id for i in iterator]


def test_scan_artworks_eval_bbb(
    artwork_aaa: ArtWork, artwork_bbb: ArtWork, artwork_ccc: ArtWork
):
    """bbbよりあとの作品一覧取得"""
    iterator: ResultIterator[ArtWork] = ArtWork.scan_artworks(
        last_evaluated_id=artwork_bbb.id
    )

    assert [artwork_ccc.id] == [i.id for i in iterator]
