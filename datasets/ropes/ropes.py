# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and DataLab Authors.
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
"""ROPES dataset.
Code is heavily inspired from https://github.com/huggingface/datalabs/blob/master/datalabs/squad/squad.py"""


import json

import datalabs
from datalabs import get_task, TaskType

_CITATION = """\
@inproceedings{Lin2019ReasoningOP,
  title={Reasoning Over Paragraph Effects in Situations},
  author={Kevin Lin and Oyvind Tafjord and Peter Clark and Matt Gardner},
  booktitle={MRQA@EMNLP},
  year={2019}
}
"""

_DESCRIPTION = """\
ROPES (Reasoning Over Paragraph Effects in Situations) is a QA dataset
which tests a system's ability to apply knowledge from a passage
of text to a new situation. A system is presented a background
passage containing a causal or qualitative relation(s) (e.g.,
"animal pollinators increase efficiency of fertilization in flowers"),
a novel situation that uses this background, and questions that require
reasoning about effects of the relationships in the background
passage in the background of the situation.
"""

_LICENSE = "CC BY 4.0"

_URLs = {
    "train+dev": "https://ropes-dataset.s3-us-west-2.amazonaws.com/train_and_dev/ropes-train-dev-v1.0.tar.gz",
    "test": "https://ropes-dataset.s3-us-west-2.amazonaws.com/test/ropes-test-questions-v1.0.tar.gz",
}


class Ropes(datalabs.GeneratorBasedBuilder):
    """ROPES datset: testing a system's ability
    to apply knowledge from a passage of text to a new situation.."""

    VERSION = datalabs.Version("1.1.0")

    BUILDER_CONFIGS = [
        datalabs.BuilderConfig(name="plain_text", description="Plain text", version=VERSION),
    ]

    def _info(self):
        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=datalabs.Features(
                {
                    "id": datalabs.Value("string"),
                    # "background": datalabs.Value("string"),
                    "title": datalabs.Value("string"),
                    "url": datalabs.Value("string"),
                    "context": datalabs.Value("string"),
                    "situation": datalabs.Value("string"),
                    "question": datalabs.Value("string"),
                    "answers":
                        {
                            "text": datalabs.features.Sequence(datalabs.Value("string")),
                            "answer_start": datalabs.features.Sequence(datalabs.Value("int32")),
                        }
                }
            ),
            supervised_keys=None,
            homepage="https://allenai.org/data/ropes",
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[
                get_task(TaskType.qa_extractive)(
                    question_column="question", context_column="context", answers_column="answers"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archives = dl_manager.download(_URLs)

        return [
            datalabs.SplitGenerator(
                name=datalabs.Split.TRAIN,
                gen_kwargs={
                    "filepath": "/".join(["ropes-train-dev-v1.0", "train-v1.0.json"]),
                    "split": "train",
                    "files": dl_manager.iter_archive(archives["train+dev"]),
                },
            ),
            datalabs.SplitGenerator(
                name=datalabs.Split.TEST,
                gen_kwargs={
                    "filepath": "/".join(["ropes-test-questions-v1.0", "test-1.0.json"]),
                    "split": "test",
                    "files": dl_manager.iter_archive(archives["test"]),
                },
            ),
            datalabs.SplitGenerator(
                name=datalabs.Split.VALIDATION,
                gen_kwargs={
                    "filepath": "/".join(["ropes-train-dev-v1.0", "dev-v1.0.json"]),
                    "split": "dev",
                    "files": dl_manager.iter_archive(archives["train+dev"]),
                },
            ),
        ]

    def _generate_examples(self, filepath, split, files):
        """Yields examples."""
        for path, f in files:
            if path == filepath:
                ropes = json.loads(f.read().decode("utf-8"))
                for article in ropes["data"]:
                    for paragraph in article["paragraphs"]:
                        background = paragraph["background"].strip()
                        situation = paragraph["situation"].strip()
                        for qa in paragraph["qas"]:
                            question = qa["question"].strip()
                            id_ = qa["id"]
                            answers = [] if split == "test" else [answer["text"].strip() for answer in qa["answers"]]
                            yield id_, {
                                "title": "title",
                                "context": background,
                                "situation": situation,
                                "question": question,
                                "id": id_,
                                "answers": {
                                    "answer_start": [-1]*len(answers),
                                    "text": answers,
                                },
                                "url": "xxx",
                            }
                            #
                            # answers = {}
                            # if split == "test":
                            #     answers = {
                            #         "text": None,
                            #         "answer_start": None
                            #     }
                            # else:
                            #     answers = [{"text": res_info["text"].strip(), "answer_start":-1} for res_info in qa["answers"]]
                            # yield id_, {
                            #     "title": "title",
                            #     "context": background,
                            #     "situation": situation,
                            #     "question": question,
                            #     "id": id_,
                            #     "answers": answers,
                            #     "url": "xxx",
                            # }

                break