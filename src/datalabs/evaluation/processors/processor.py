from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Optional

from datalabs.features import features
from datalabs.info import SysOutputInfo
from datalabs.tasks.task_info import TaskType


class Processor:
    """Base case for task-based processor"""

    _features: features.Features
    _task_type: TaskType

    def __init__(self, metadata: dict, system_output_data: Iterable[dict]) -> None:
        self._metadata = {**metadata, "features": self._features}
        self._system_output_info = SysOutputInfo.from_dict(self._metadata)
        # should really be a base type of builders
        self._builder: Optional[Any] = None

    def process(self) -> SysOutputInfo:
        if not self._builder:
            raise NotImplementedError
        return self._builder.run()
