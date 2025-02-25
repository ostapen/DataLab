import csv
import json

import datalabs

from datalabs.utils.logging import get_logger
from datalabs import get_task, TaskType

logger = get_logger(__name__)


_CITATION = """
@inproceedings{yin2018learning,
  title={Learning to mine aligned code and natural language pairs from stack overflow},
  author={Yin, Pengcheng and Deng, Bowen and Chen, Edgar and Vasilescu, Bogdan and Neubig, Graham},
  booktitle={2018 IEEE/ACM 15th international conference on mining software repositories (MSR)},
  pages={476--486},
  year={2018},
  organization={IEEE}
}
"""


_DESCRIPTION = """\
CoNaLa was designed to test systems for generating program snippets from natural
language. For example, if the input is sort list x in reverse order, then the system
would be required to output x.sort(reverse=True) in Python. It includes a dataset
crawled from Stack Overflow, automatically filtered, then curated by annotators, split
into 2,379 training and 500 test examples (read more about the process here). It also
includes a large automatically-mined dataset with 600k examples, and links to other
similar datasets.
"""

dataset_url = "http://www.phontron.com/download/conala-corpus-v1.1.zip"


class ConalaConfig(datalabs.BuilderConfig):
    """BuilderConfig for Conala."""

    def __init__(self, **kwargs):
        """BuilderConfig for Conala.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ConalaConfig, self).__init__(**kwargs)


class Conala(datalabs.GeneratorBasedBuilder):

    def _info(self):
        features_dataset = datalabs.Features()
        features_sample = datalabs.Features(
            {
                "question_id": datalabs.Value("int32"),
                "orig_en": datalabs.Value("string"),
                "translation": {
                    "en": datalabs.Value("string"),
                    "python": datalabs.Value("string"),
                }
            }
        )

        return datalabs.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=features_sample,
            features_dataset=features_dataset,
            supervised_keys=None,
            homepage="https://conala-corpus.github.io/",
            citation=_CITATION,
            languages=['en', 'python'],
            task_templates=[
                get_task(TaskType.code_generation)(
                    translation_column="translation",
                    lang_sub_columns=["en", "python"],
                )
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dataset_path = dl_manager.download_and_extract(dataset_url)

        split_gens = [
            datalabs.SplitGenerator(
                name=datalabs.Split.TRAIN,
                gen_kwargs={"filepath": f'{dataset_path}/conala-corpus/conala-train.json'},
            ),
            datalabs.SplitGenerator(
                name=datalabs.Split.TEST,
                gen_kwargs={"filepath": f'{dataset_path}/conala-corpus/conala-test.json'},
            ),
            datalabs.SplitGenerator(
                name='mined',
                gen_kwargs={
                    "filepath": f'{dataset_path}/conala-corpus/conala-mined.jsonl'},
            ),
        ]
        return split_gens

    def _convert_data(self, data):
        return {
            "question_id": data['question_id'],
            "orig_en": data['intent'],
            "translation": {
                "en": data['rewritten_intent'],
                "python": data['snippet'],
            }
        }

    def _generate_examples(self, filepath):
        """Yields examples."""
        id_sample = 0
        if 'jsonl' in filepath:
            with open(filepath, encoding="utf-8") as fin:
                for _id, line in enumerate(fin):
                    data = json.loads(line)
                    data['rewritten_intent'] = ''
                    yield _id, self._convert_data(data)
        else:
            with open(filepath, encoding="utf-8") as fin:
                for _id, data in enumerate(json.load(fin)):
                    yield _id, self._convert_data(data)
