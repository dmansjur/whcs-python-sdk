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
import configparser
import ibm_whcs_sdk.insights_for_medical_literature as wh

# To access a secure environment additional parameters are needed on the constructor which are listed below
CONFIG = configparser.RawConfigParser()
CONFIG.read('./ibm_whcs_sdk/insights_for_medical_literature/tests/config.ini')

BASE_URL = CONFIG.get('settings', 'base_url')
APIKEY = CONFIG.get('settings', 'key')
IAMURL = CONFIG.get('settings', 'iam_URL')
LEVEL = CONFIG.get('settings', 'logging_level')
VERSION = CONFIG.get('settings', 'version')
DISABLE_SSL = CONFIG.get('settings', 'disable_ssl')
CORPUS = CONFIG.get('settings', 'corpus')

IML_TEST = wh.InsightsForMedicalLiteratureServiceV1(BASE_URL, APIKEY, IAMURL, VERSION, LEVEL, DISABLE_SSL)

def test_get_corpus_info():
    response = IML_TEST.get_corpus_config(corpus=CORPUS)
    corpora_config_model = wh.CorporaConfigModel._from_dict(response.get_result())
    corpus_list = corpora_config_model.corpora
    for item in corpus_list:
        assert item.corpus_name is not None
        assert item.ontologies is not None

def test_get_corpus_info_verbose():
    response = IML_TEST.get_corpus_config(corpus=CORPUS, verbose=True)
    corpora_config_model = wh.CorporaConfigModel._from_dict(response.get_result())
    corpus_list = corpora_config_model.corpora
    for item in corpus_list:
        assert item.corpus_name is not None
        assert item.ontologies is not None

def test_get_corpus_info_no_corpus():
    try:
        IML_TEST.get_corpus_config(corpus=None)
    except ValueError as exp:
        assert exp is not None
