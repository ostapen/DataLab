# coding=utf-8
# Copyright 2020 The TensorFlow datasets Authors and the HuggingFace datasets, DataLab Authors.
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

import json
import datalabs
from datalabs import get_task, TaskType

_DESCRIPTION = """\
CAIL2019 contains a total of 10,000 groups of triple texts, which come from the factual description part of private lending cases.
The goal of the task is to determine whether text0 is more similar to text1 or more similar to text2. 
"""

_CITATION = """\
@article{xiao2019cail2019,
  title={CAIL2019-SCM: A Dataset of Similar Case Matching in Legal Domain},
  author={Xiao, Chaojun and Zhong, Haoxi and Guo, Zhipeng and Tu, Cunchao and Liu, Zhiyuan and Sun, Maosong and Zhang, Tianyang and Han, Xianpei and Wang, Heng and Xu, Jianfeng and others},
  journal={arXiv preprint arXiv:1911.08962},
  year={2019}
}
"""

_LICENSE = "NA"

_TRAIN_DOWNLOAD_URL = "http://cdatalab1.oss-cn-beijing.aliyuncs.com/text_matching/CAIL2019-SCM/train.json"
_VALIDATION_DOWNLOAD_URL = "http://cdatalab1.oss-cn-beijing.aliyuncs.com/text_matching/CAIL2019-SCM/valid.json"
_TEST_DOWNLOAD_URL = "http://cdatalab1.oss-cn-beijing.aliyuncs.com/text_matching/CAIL2019-SCM/test.json"

_HOMEPAGE = "https://github.com/china-ai-law-challenge/CAIL2019/tree/master/scm"


class CAIL2019Config(datalabs.BuilderConfig):
    
    def __init__(self, **kwargs):

        super(CAIL2019Config, self).__init__(**kwargs)

class CAIL2019(datalabs.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        CAIL2019Config(
            name="text_matching_multiple_choice",
            version=datalabs.Version("1.0.0"),
            description="text_matching_multiple_choice",
        ),
    ]

    DEFAULT_CONFIG_NAME = "text_matching_multiple_choice"

    def _info(self):

        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=datalabs.Features(
                {
                    "text": datalabs.Value("string"),
                    "options": datalabs.features.Sequence(datalabs.Value("string")),
                    "label": datalabs.features.ClassLabel(names=["0", "1"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            languages=["zh"],
            task_templates=[
                get_task(TaskType.text_matching_multiple_choice)(
                    text_column = "text",
                    options_column = "options",
                    label_column = "label",
                ),
            ],
        )

    def _split_generators(self, dl_manager):

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        validation_path = dl_manager.download_and_extract(_VALIDATION_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        
        return [
            datalabs.SplitGenerator(name=datalabs.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datalabs.SplitGenerator(name=datalabs.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datalabs.SplitGenerator(name=datalabs.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        labels = {
            "B": "0",
            "C": "1",
        }
        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                line = json.loads(line)
                text = line["A"].rstrip()
                options = [line["B"].rstrip(), line["C"].rstrip()]
                label = line["label"]
                if label in labels:
                    yield id_, {"text": text, "options": options, "label": labels[label]}