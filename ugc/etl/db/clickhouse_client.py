from clickhouse_driver import Client
from config import settings

from .backoff import backoff

client = Client(host=settings.CLICKHOUSE_SERVER)


@backoff("Clickhouse.insert")
def insert_views(data):
    """
    INSERT INTO ugc_data.user_movie_progress
    Table fields
        user_id    String,
        movie_id   String,
        time       UInt16,
        percent    Float32,
        event_time DateTime
    """
    SQL = "INSERT INTO ugc_data.user_movie_progress VALUES"
    print("sended")
    # client.execute(SQL, data)
