# coding=utf-8
# Copyright 2022 The DataLab authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""The WNUT 17 Emerging Entities Dataset."""


import datalabs
from datalabs import get_task, TaskType

logger = datalabs.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{derczynski-etal-2017-results,
    title = "Results of the {WNUT}2017 Shared Task on Novel and Emerging Entity Recognition",
    author = "Derczynski, Leon  and
      Nichols, Eric  and
      van Erp, Marieke  and
      Limsopatham, Nut",
    booktitle = "Proceedings of the 3rd Workshop on Noisy User-generated Text",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-4418",
    doi = "10.18653/v1/W17-4418",
    pages = "140--147",
    abstract = "This shared task focuses on identifying unusual, previously-unseen entities in the context of emerging discussions.
                Named entities form the basis of many modern approaches to other tasks (like event clustering and summarization),
                but recall on them is a real problem in noisy text - even among annotators.
                This drop tends to be due to novel entities and surface forms.
                Take for example the tweet {``}so.. kktny in 30 mins?!{''} {--} even human experts find the entity {`}kktny{'}
                hard to detect and resolve. The goal of this task is to provide a definition of emerging and of rare entities,
                and based on that, also datalab for detecting these entities. The task as described in this paper evaluated the
                ability of participating entries to detect and classify novel and emerging named entities in noisy text.",
}
"""

_DESCRIPTION = """\
WNUT 17: Emerging and Rare entity recognition

This shared task focuses on identifying unusual, previously-unseen entities in the context of emerging discussions.
Named entities form the basis of many modern approaches to other tasks (like event clustering and summarisation),
but recall on them is a real problem in noisy text - even among annotators. This drop tends to be due to novel entities and surface forms.
Take for example the tweet “so.. kktny in 30 mins?” - even human experts find entity kktny hard to detect and resolve.
This task will evaluate the ability to detect and classify novel, emerging, singleton named entities in noisy text.

The goal of this task is to provide a definition of emerging and of rare entities, and based on that, also datalab for detecting these entities.
"""

_URL = "https://raw.githubusercontent.com/leondz/emerging_entities_17/master/"
_TRAINING_FILE = "wnut17train.conll"
_DEV_FILE = "emerging.dev.conll"
_TEST_FILE = "emerging.test.annotated"







class WNUT_17Config(datalabs.BuilderConfig):
    """The WNUT 17 Emerging Entities Dataset."""

    def __init__(self, **kwargs):
        """BuilderConfig for WNUT 17.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(WNUT_17Config, self).__init__(**kwargs)




class WNUT_17(datalabs.GeneratorBasedBuilder):
    """The WNUT 17 Emerging Entities Dataset."""



    # def __init__(self,*args, **kwargs):
    #     super(WNUT_17, self).__init__(*args, **kwargs)
    #     self.dataset_class = SequenceLabelingDataset




    BUILDER_CONFIGS = [
        WNUT_17Config(
            name="wnut_17", version=datalabs.Version("1.0.0"), description="The WNUT 17 Emerging Entities Dataset"
        ),
    ]

    def _info(self):
        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=datalabs.Features(
                {
                    "id": datalabs.Value("string"),
                    "tokens": datalabs.Sequence(datalabs.Value("string")),
                    "tags": datalabs.Sequence(
                        datalabs.features.ClassLabel(
                            names=[
                                "O",
                                "B-corporation",
                                "I-corporation",
                                "B-creative-work",
                                "I-creative-work",
                                "B-group",
                                "I-group",
                                "B-location",
                                "I-location",
                                "B-person",
                                "I-person",
                                "B-product",
                                "I-product",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="http://noisy-text.github.io/2017/emerging-rare-entities.html",
            citation=_CITATION,
            task_templates=[get_task(TaskType.named_entity_recognition)(
                tokens_column="tokens",
                tags_column="tags")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datalabs.SplitGenerator(name=datalabs.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datalabs.SplitGenerator(name=datalabs.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datalabs.SplitGenerator(name=datalabs.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            current_tokens = []
            current_labels = []
            sentence_counter = 0
            for row in f:
                row = row.rstrip()
                if row:
                    token, label = row.split("\t")
                    current_tokens.append(token)
                    current_labels.append(label)
                else:
                    # New sentence
                    if not current_tokens:
                        # Consecutive empty lines will cause empty sentences
                        continue
                    assert len(current_tokens) == len(current_labels), "💔 between len of tokens & labels"
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_tokens,
                            "tags": current_labels,
                        },
                    )
                    sentence_counter += 1
                    current_tokens = []
                    current_labels = []
                    yield sentence
            # Don't forget last sentence in dataset 🧐
            if current_tokens:
                yield sentence_counter, {
                    "id": str(sentence_counter),
                    "tokens": current_tokens,
                    "tags": current_labels,
                }
