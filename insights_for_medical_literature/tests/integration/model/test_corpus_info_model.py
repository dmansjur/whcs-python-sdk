# coding: utf-8

# Copyright 2018 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import watson_health_cognitive_services.insights_for_medical_literature as wh


def test_corpus_info_model():
    providers = []
    model = wh.CorpusInfoModel(document_count=100, providers=providers)
    model_diff = wh.CorpusInfoModel(document_count=200, providers=providers)
    model_same = wh.CorpusInfoModel(document_count=100, providers=providers)

    assert model.__str__() is not None
    assert model.__eq__(model_same)
    assert model.__ne__(model_diff)
