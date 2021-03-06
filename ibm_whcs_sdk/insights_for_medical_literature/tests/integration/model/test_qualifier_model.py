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

import ibm_whcs_sdk.insights_for_medical_literature as wh

def test_qualifier_model():
    qualifier_obj = {}
    qualifier_obj['qualifier_id'] = 'test'
    qualifier_obj['qualifier_name'] = 'test'

    qualifier = wh.Qualifier('test', 'test')
    qualifier_diff = wh.Qualifier('test', 'exam')
    qualifier_dict = qualifier._from_dict(qualifier_obj)

    assert qualifier.__str__()
    assert qualifier.__eq__(qualifier_dict)
    assert qualifier.__ne__(qualifier_diff)
