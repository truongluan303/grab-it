from __future__ import annotations

import datetime
import logging
import os
import threading
from time import sleep


_logger = logging.getLogger(__name__)


EXPIRED_MINS = 10


class TempfilesManager:
    __instance = None

    @classmethod
    def get_instance(cls) -> TempfilesManager:
        return cls() if cls.__instance == None else cls.__instance

    def __init__(self) -> None:
        if TempfilesManager.__instance != None:
            raise Exception(
                "Cannot re-initialize singleton class! Use get_instance instead!"
            )

        self._files: dict[str, str] = dict()
        self._files_timestamp: dict[str, datetime.datetime] = dict()

        # Constantly check for expired files in a different thread
        threading.Thread(target=self.__watch_for_expired_files).start()

        TempfilesManager.__instance = self
        _logger.info("singleton TempFileManager is initialized!")

    def contains(self, file_id: str) -> bool:
        return file_id in self._files

    def add_file(self, file_id: str, file_path: str) -> bool:
        if file_id in self._files:
            return False
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f'File with ID "{file_id}" and path "{file_path}" is not found!'
            )

        self._files[file_id] = file_path
        self._files_timestamp[file_id] = datetime.datetime.now()
        return True

    def get_file(self, file_id: str) -> str | None:
        return self._files.get(file_id)

    def remove_file(self, file_id: str) -> bool:
        if file_id not in self._files or not os.path.exists(self._files[file_id]):
            return False

        self._files_timestamp.pop(file_id, None)
        os.remove(self._files.pop(file_id))
        return True

    def prevent_expiration_removal(self, file_id: str) -> bool:
        if file_id not in self._files:
            return False

        self._files_timestamp.pop(file_id, None)
        return True

    def __watch_for_expired_files(self) -> None:
        while True:
            files_to_remove: list[str] = []
            sleep_time_in_secs = 60 * EXPIRED_MINS

            for file_id, timestamp in self._files_timestamp.items():
                timediff: datetime.timedelta = datetime.datetime.now() - timestamp
                timediff_in_mins = timediff.total_seconds() / 60

                if timediff_in_mins >= EXPIRED_MINS:
                    files_to_remove.append(file_id)
                else:
                    sleep_time_in_secs -= timediff_in_mins

            if files_to_remove:
                threading.Thread(target=self.__prune_files(files_to_remove))
            sleep(sleep_time_in_secs)

    def __prune_files(self, files: list[str]) -> None:
        paths = [self._files[fileid] for fileid in files]

        [self.remove_file(file_id) for file_id in files]
        [os.remove(path) for path in paths if os.path.exists(path)]
