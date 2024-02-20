import logging
from celery import shared_task
from apps.common.models import File
from services.synchronizer import Synchronizer

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def synchronizer(
        self,
        file_identifier,
        columns_to_rename=None,
        values_to_replace=None,
        merge_columns=None,
        sheet_mapping=None,
        file_mapping=None,
        file_name=None
):
    synchronizer_instance = Synchronizer(
        file_identifier=file_identifier,
        columns_to_rename=columns_to_rename,
        values_to_replace=values_to_replace,
        multiple_sheets=sheet_mapping,
        merge_columns=merge_columns,
        file_mapping=file_mapping,
        file_name=file_name
    )
    synchronizer_instance.run()
    File.objects.get(file_identifier=file_identifier).delete()

    return "Synchronization completed successfully."
    # except Exception as e:
    #     logger.exception("Error occurred during synchronization:")
    #     raise e
