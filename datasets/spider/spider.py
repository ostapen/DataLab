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
"""Spider: A Large-Scale Human-Labeled Dataset for Text-to-SQL Tasks"""


import json
import os
import datalabs
from datalabs import get_task, TaskType


# logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{yu2018spider,
  title={Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-sql task},
  author={Yu, Tao and Zhang, Rui and Yang, Kai and Yasunaga, Michihiro and Wang, Dongxu and Li, Zifan and Ma, James and Li, Irene and Yao, Qingning and Roman, Shanelle and others},
  journal={arXiv preprint arXiv:1809.08887},
  year={2018}
}
"""

_DESCRIPTION = """\
Spider is a large-scale complex and cross-domain semantic parsing and text-toSQL dataset annotated by 11 college students
"""

_HOMEPAGE = "https://yale-lily.github.io/spider"

_LICENSE = "CC BY-SA 4.0"

_URL = "https://drive.google.com/uc?export=download&id=1_AckYkinAnhqmRQtGsQgUKAnTHxxX5J0&confirm=yes"


class Spider(datalabs.GeneratorBasedBuilder):
    VERSION = datalabs.Version("1.0.0")

    BUILDER_CONFIGS = [
        datalabs.BuilderConfig(
            name="spider",
            version=VERSION,
            description="Spider: A Large-Scale Human-Labeled Dataset for Text-to-SQL Tasks",
        ),
    ]

    def _info(self):
        features = datalabs.Features(
            {
                "db_id": datalabs.Value("string"),
                "query": datalabs.Value("string"),
                "question": datalabs.Value("string"),
                "query_toks": datalabs.features.Sequence(datalabs.Value("string")),
                "query_toks_no_value": datalabs.features.Sequence(datalabs.Value("string")),
                "question_toks": datalabs.features.Sequence(datalabs.Value("string")),
            }
        )
        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[
                get_task(TaskType.text_to_sql)(
                    question_column="question",
                    query_column="query"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        downloaded_filepath = dl_manager.download_and_extract(_URL)

        return [
            datalabs.SplitGenerator(
                name=datalabs.Split.TRAIN,
                gen_kwargs={
                    "data_filepath": os.path.join(downloaded_filepath, "spider/train_spider.json"),
                },
            ),
            datalabs.SplitGenerator(
                name=datalabs.Split.VALIDATION,
                gen_kwargs={
                    "data_filepath": os.path.join(downloaded_filepath, "spider/dev.json"),
                },
            ),
        ]

    def _generate_examples(self, data_filepath):
        """This function returns the examples in the raw (text) form."""
        # logger.info("generating examples from = %s", data_filepath)
        with open(data_filepath, encoding="utf-8") as f:
            spider = json.load(f)
            for idx, sample in enumerate(spider):
                yield idx, {
                    "db_id": sample["db_id"],
                    "query": sample["query"],
                    "question": sample["question"],
                    "query_toks": sample["query_toks"],
                    "query_toks_no_value": sample["query_toks_no_value"],
                    "question_toks": sample["question_toks"],
                }
