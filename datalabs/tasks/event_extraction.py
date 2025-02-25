from dataclasses import dataclass
from typing import ClassVar

from datalabs.features import Features, Sequence, Value
from datalabs.tasks.base import register_task, TaskTemplate, TaskType


@register_task(TaskType.event_extraction)
@dataclass
class EventExtraction(TaskTemplate):
    task: TaskType = TaskType.event_extraction
    text_column: str = "text"
    event_column: str = "event"

    def __post_init__(self):
        self.task_categories = [
            task_cls.get_task() for task_cls in self.get_task_parents()
        ]
        if self.input_schema is None:
            self.input_schema: ClassVar[Features] = Features(
                {"text": Value("string")}
            )
        if self.label_schema is None:
            self.label_schema: ClassVar[Features] = Features(
                {"event": Value("string")}
            )


@register_task(TaskType.event_entity_extraction)
@dataclass
class EventEntityExtraction(EventExtraction):
    task: TaskType = TaskType.event_entity_extraction

    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    label_schema: ClassVar[Features] = Features({"event_entity": Value("string")})

    text_column: str = "text"
    event_column: str = "event_entity"

@register_task(TaskType.event_arguments_extraction)
@dataclass
class EventArgumentsExtraction(EventExtraction):
    task: TaskType = TaskType.event_arguments_extraction

    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    label_schema: ClassVar[Features] = Features({"arguments": Sequence(Value("string"))})

    text_column: str = "text"
    event_column: str = "arguments"

@register_task(TaskType.event_relation_extraction)
@dataclass
class EventRelationExtraction(EventExtraction):
    task: TaskType = TaskType.event_relation_extraction

    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    label_schema: ClassVar[Features] = Features({"relation": Sequence(Value("string"))})

    text_column: str = "text"
    event_column: str = "relation"



