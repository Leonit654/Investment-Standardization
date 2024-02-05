import logging
from celery import shared_task
from .synchronizer import Synchronizer

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def synchronizer(self, file_identifier, file_type, columns_to_rename=None, values_to_replace=None, merge_columns=None):
    try:
        synchronizer_instance = Synchronizer(
            file_identifier=file_identifier,
            file_type=file_type,
            columns_to_rename=columns_to_rename,
            values_to_replace=values_to_replace,
            multiple_sheets=None,
            merge_columns=merge_columns
        )
        synchronizer_instance.run()
    except Exception as e:
        logger.exception("Error occurred during synchronization:")
        raise e
