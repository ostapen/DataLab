# coding=utf-8
# Copyright 2022 DataLab Authors and the current dataset script contributor.
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
import os
import datalabs
from datalabs import get_task, TaskType
logger = datalabs.logging.get_logger(__name__)

_CITATION = """\

"""
_DESCRIPTION = """\
Weibo_Named Entity Recognition
"""
_HOMEPAGE = "https://github.com/OYE93/Chinese-NLP-Corpus/"
_LICENSE = "Available for research use"

_TRAIN_DOWNLOAD_URL = "https://cdatalab1.oss-cn-beijing.aliyuncs.com/ner/Weibo/weiboNER_2nd_conll.train"
_VALIDATION_DOWNLOAD_URL = "https://cdatalab1.oss-cn-beijing.aliyuncs.com/ner/Weibo/weiboNER_2nd_conll.dev"
_TEST_DOWNLOAD_URL = "https://cdatalab1.oss-cn-beijing.aliyuncs.com/ner/Weibo/weiboNER_2nd_conll.test"


class WeiboNER(datalabs.GeneratorBasedBuilder):


    VERSION = datalabs.Version("1.0.0")



    def _info(self):
        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=datalabs.Features(
                {
                    "id": datalabs.Value("string"),
                    "tokens": datalabs.Sequence(datalabs.Value("string")),
                    "tags": datalabs.Sequence(
                        datalabs.features.ClassLabel(
                            names=['O','B-PER.NAM','I-PER.NAM',
                            'B-PER.NOM',
                            'I-PER.NOM',
                            'B-LOC.NAM',
                            'I-LOC.NAM',
                            'B-LOC.NOM',
                            'I-LOC.NOM',
                            'B-GPE.NAM',
                            'I-GPE.NAM',
                            'B-GPE.NOM',
                            'I-GPE.NOM',
                            'B-ORG.NOM',
                            'I-ORG.NOM',
                            'B-ORG.NAM',
                            'I-ORG.NAM'
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
            languages=['zh'],
            version=self.VERSION,
            task_templates=[get_task(TaskType.named_entity_recognition)
                                        (tokens_column="tokens", tags_column="tags")],
        )

    def _split_generators(self, dl_manager):
        
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        validation_path = dl_manager.download_and_extract(_VALIDATION_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        
        return [
            datalabs.SplitGenerator(name=datalabs.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datalabs.SplitGenerator(name=datalabs.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datalabs.SplitGenerator(name=datalabs.Split.TEST, gen_kwargs={"filepath": test_path})
        ]
        

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            current_tokens = []
            current_labels = []
            sentence_counter = 0

            for row in f:
                row = row.strip()
                if row!="":
                    
                    span_list = row.split('\t')
                    token = ''.join(list(span_list[0])[:-1])
                    label= span_list[-1]
                    current_tokens.append(token)
                    current_labels.append(label)
                else:  
                    # New sentence
                    if not current_tokens:
                   
                        continue
                    assert len(current_tokens) == len(current_labels), "mismatch between len of tokens & labels"
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
   
            if current_tokens:
                yield sentence_counter, {
                    "id": str(sentence_counter),
                    "tokens": current_tokens,
                    "tags": current_labels,
                }
