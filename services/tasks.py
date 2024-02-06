import logging
from celery import shared_task
from apps.common.models import File
from .synchronizer import Synchronizer
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def synchronizer(self, file_identifier, file_type=None, columns_to_rename=None, values_to_replace=None, merge_columns=None, sheet_mapping=None):
    try:
        logger.info(f"Sheeeeeeeeeeeeet mappinggggggg- {sheet_mapping}")
        synchronizer_instance = Synchronizer(
            file_identifier=file_identifier,
            file_type=file_type,
            columns_to_rename=columns_to_rename,
            values_to_replace=values_to_replace,
            multiple_sheets=sheet_mapping,
            merge_columns=merge_columns,
        )
        synchronizer_instance.run()
        File.objects.get(file_identifier=file_identifier).delete()
        return "Synchronization started successfully."
    except Exception as e:
        logger.exception("Error occurred during synchronization:")
        raise e