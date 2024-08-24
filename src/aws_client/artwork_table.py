from typing import Any, Optional
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.pagination import ResultIterator

from typeguard import typechecked


@typechecked
class ArtWork(Model):
    class Meta:
        table_name = "Artwork"  # FIXME: 環境変数などでインフラに合わせる
        region = "ap-northeast-1"
        write_capacity_units = 10
        read_capacity_units = 10

    id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute(null=False)
    good = NumberAttribute(default_for_new=0)
    body = UnicodeAttribute(default_for_new="")

    @classmethod
    def scan_artworks(
        cls, last_evaluated_id: Optional[str] = None, page_size: Optional[int] = None
    ) -> ResultIterator["ArtWork"]:
        """記事一覧を取得"""
        last_evaluated_key: dict[str, dict[str, Any]] | None = (
            {"id": {"S": last_evaluated_id}} if last_evaluated_id else None
        )
        return ArtWork.scan(
            attributes_to_get=["id", "body"],
            last_evaluated_key=last_evaluated_key,
            page_size=page_size,
        )
