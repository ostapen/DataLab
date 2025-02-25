# coding=utf-8
# Copyright 2022 The HuggingFace datasets Authors, DataLab Authors and the current dataset script contributor.
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
"""The Yelp Review Full dataset for text classification."""


import csv
import os
import datalabs
from datalabs import get_task, TaskType


_CITATION = """\
@inproceedings{zhang2015character,
  title={Character-level convolutional networks for text classification},
  author={Zhang, Xiang and Zhao, Junbo and LeCun, Yann},
  booktitle={Advances in neural information processing systems},
  pages={649--657},
  year={2015}
}
"""

_DESCRIPTION = """\
The Yelp reviews dataset consists of reviews from Yelp. It is extracted from the Yelp Dataset Challenge 2015 data.
The Yelp reviews full star dataset is constructed by Xiang Zhang (xiang.zhang@nyu.edu) from the above dataset.
It is first used as a text classification benchmark in the following paper: Xiang Zhang, Junbo Zhao, Yann LeCun.
Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).
"""

_HOMEPAGE = "https://www.yelp.com/dataset"

_LICENSE = "https://s3-media3.fl.yelpcdn.com/assets/srv0/engineering_pages/bea5c1e92bf3/assets/vendor/yelp-dataset-agreement.pdf"

_URLs = {
    "yelp_review_full": "https://drive.google.com/uc?export=download&id=0Bz8a_Dbh9QhbZlU4dXhHTFhZQU0&confirm=yes",
}


class YelpReviewFullConfig(datalabs.BuilderConfig):
    """BuilderConfig for YelpReviewFull."""

    def __init__(self, **kwargs):
        """BuilderConfig for YelpReviewFull.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(YelpReviewFullConfig, self).__init__(**kwargs)


class YelpReviewFull(datalabs.GeneratorBasedBuilder):
    """Yelp Review Full Star Dataset 2015."""

    VERSION = datalabs.Version("1.0.0")

    BUILDER_CONFIGS = [
        YelpReviewFullConfig(
            name="yelp_review_full", version=VERSION, description="Yelp Review Full Star Dataset 2015"
        ),
    ]

    def _info(self):
        features = datalabs.Features(
            {
                "label": datalabs.features.ClassLabel(
                    names=[
                        "1 star",
                        "2 star",
                        "3 stars",
                        "4 stars",
                        "5 stars",
                    ]
                ),
                "text": datalabs.Value("string"),
            }
        )
        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[get_task(TaskType.sentiment_classification)(
                text_column="text",
                label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datalabs.SplitGenerator(
                name=datalabs.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "yelp_review_full_csv", "train.csv"),
                    "split": "train",
                },
            ),
            datalabs.SplitGenerator(
                name=datalabs.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "yelp_review_full_csv", "test.csv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""



        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
            for id_, row in enumerate(data):
                yield id_, {
                    "text": row[1],
                    "label": int(row[0]) - 1,
                }
