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
import ibm_whcs_sdk.annotator_for_clinical_data as wh
import test_unstructured_container as tuc

CONFIG = configparser.RawConfigParser()
CONFIG.read('./ibm_whcs_sdk/annotator_for_clinical_data/tests/config.ini')

BASE_URL = CONFIG.get('settings', 'base_url')
APIKEY = CONFIG.get('settings', 'key')
IAMURL = CONFIG.get('settings', 'iam_url')
VERSION = CONFIG.get('settings', 'version')
LEVEL = CONFIG.get('settings', 'logging_level')
DISABLE_SSL = CONFIG.get('settings', 'disable_ssl')
FLOW = CONFIG.get('settings', 'flow')

ACD = wh.AnnotatorForClinicalDataV1(BASE_URL, APIKEY, IAMURL, VERSION, LEVEL, DISABLE_SSL)

LINE1 = 'The patient has cancer and is currently taking 400 ml sisplatin chemotherapy.\n'
LINE2 = 'HISTORY:  Patient is allergic to latex.  Patient cannot walk and needs help bathing and getting around.  '
LINE3 = 'The lab values were: white blood cell count 4.6, hemoglobin 12.2.  '
LINE4 = 'Echocardiogram demonstrated ejection fraction of approx 60%.  '
LINE5 = 'Patient cannot dress or feed without help as the patient can not see.  Patient may die soon but has not '
LINE6 = 'died yet.  Patient smoked for 20 years.  Patient can not clean up after defacating in toilet.  '
LINE7 = 'Jone Doe was seen at Baylor Hospitall in Austin, TX.  Johndoe@testaddress.com - (555) 555-5555'
TEXT = LINE1 + LINE2 + LINE3 + LINE4 + LINE5 + LINE6 + LINE7

def test_analyze_flow():
    data = ACD.analyze_with_flow(FLOW, TEXT)
    tuc.TestUnstructuredContainer.test_unstructured_container(data=data)

def test_analyze_flow_container():
    container = wh.UnstructuredContainer(TEXT)
    data = ACD.analyze_with_flow(FLOW, container)
    tuc.TestUnstructuredContainer.test_unstructured_container(data=data)

def test_analyze_flow_request_list():
    container = [wh.UnstructuredContainer(TEXT)]
    container_group = ACD.analyze_with_flow(FLOW, container)

    for unstructured_container in container_group.unstructured:
        if unstructured_container.text is not None:
            assert unstructured_container.text == TEXT
        if unstructured_container.id is not None:
            assert unstructured_container.id != '0'
        if unstructured_container.type is not None:
            assert unstructured_container.type != 'bogus'
        
        assert unstructured_container.data is not None
        tuc.TestUnstructuredContainer.test_unstructured_container(data=unstructured_container.data)

def test_analyze_flow_org():
    response = ACD.analyze_with_flow_org(FLOW, TEXT)
    container_group = wh.ContainerGroup._from_dict(response.get_result())

    for unstructured_container in container_group.unstructured:
        if unstructured_container.text is not None:
            assert unstructured_container.text == TEXT
        if unstructured_container.id is not None:
            assert unstructured_container.id != '0'
        if unstructured_container.type is not None:
            assert unstructured_container.type != 'bogus'
        
        assert unstructured_container.data is not None
        tuc.TestUnstructuredContainer.test_unstructured_container(unstructured_container.data)

def test_analyze_flow_org_json():
    container = {}
    text = {}
    text['text'] = TEXT
    unstructured = [text]
    container['unstructured'] = unstructured

    response = ACD.analyze_with_flow_org(FLOW, container,
                                          content_type='application/json')
    container_group = wh.ContainerGroup._from_dict(response.get_result())

    for unstructured_container in container_group.unstructured:
        if unstructured_container.text is not None:
            assert unstructured_container.text == TEXT
        if unstructured_container.id is not None:
            assert unstructured_container.id != '0'
        if unstructured_container.type is not None:
            assert unstructured_container.type != 'bogus'
        
        assert unstructured_container.data is not None
        tuc.TestUnstructuredContainer.test_unstructured_container(unstructured_container.data)

def test_analyze_org():

    config_entry = wh.ConfigurationEntity(id='test', type='test', uid=99)
    configs = [config_entry]

    allergy_annotator = wh.Annotator(name=wh.Name.ALLERGY)
    attr_detect_annotator = wh.Annotator(name=wh.Name.ATTRIBUTE_DETECTION)
    bathing_annotator = wh.Annotator(name=wh.Name.BATHING_ASSISTANCE)
    cancer_annotator = wh.Annotator(name=wh.Name.CANCER)
    concept_detect_annotator = wh.Annotator(name=wh.Name.CONCEPT_DETECTION)
    disambig_annotator = wh.Annotator(name=wh.Name.DISAMBIGUATION)
    dressing_annotator = wh.Annotator(name=wh.Name.DRESSING_ASSISTANCE)
    eating_annotator = wh.Annotator(name=wh.Name.EATING_ASSISTANCE)
    ef_annotator = wh.Annotator(name=wh.Name.EJECTION_FRACTION)
    hypothetical_annotator = wh.Annotator(name=wh.Name.HYPOTHETICAL)
    lab_value_annotator = wh.Annotator(name=wh.Name.LAB_VALUE)
    medication_annotator = wh.Annotator(name=wh.Name.MEDICATION)
    named_entities_annotator = wh.Annotator(name=wh.Name.NAMED_ENTITIES)
    negation_annotator = wh.Annotator(name=wh.Name.NEGATION)
    procedure_annotator = wh.Annotator(name=wh.Name.PROCEDURE)
    seeing_annotator = wh.Annotator(name=wh.Name.SEEING_ASSISTANCE)
    smoking_annotator = wh.Annotator(name=wh.Name.SMOKING)
    spelling_annotator = wh.Annotator(name=wh.Name.SPELL_CHECKER)
    symptom_disease_annotator = wh.Annotator(name=wh.Name.SYMPTOM_DISEASE)
    toileting_annotator = wh.Annotator(name=wh.Name.TOILETING_ASSISTANCE)
    walking_annotator = wh.Annotator(name=wh.Name.WALKING_ASSISTANCE)
    section = wh.Annotator(name=wh.Name.SECTION)

    flow_entries = []
    flow_entries.append(wh.FlowEntry(allergy_annotator))
    flow_entries.append(wh.FlowEntry(attr_detect_annotator))
    flow_entries.append(wh.FlowEntry(bathing_annotator))
    flow_entries.append(wh.FlowEntry(cancer_annotator))
    flow_entries.append(wh.FlowEntry(concept_detect_annotator))
    flow_entries.append(wh.FlowEntry(disambig_annotator))
    flow_entries.append(wh.FlowEntry(dressing_annotator))
    flow_entries.append(wh.FlowEntry(eating_annotator))
    flow_entries.append(wh.FlowEntry(ef_annotator))
    flow_entries.append(wh.FlowEntry(hypothetical_annotator))
    flow_entries.append(wh.FlowEntry(lab_value_annotator))
    flow_entries.append(wh.FlowEntry(medication_annotator))
    flow_entries.append(wh.FlowEntry(named_entities_annotator))
    flow_entries.append(wh.FlowEntry(negation_annotator))
    flow_entries.append(wh.FlowEntry(procedure_annotator))
    flow_entries.append(wh.FlowEntry(seeing_annotator))
    flow_entries.append(wh.FlowEntry(smoking_annotator))
    flow_entries.append(wh.FlowEntry(spelling_annotator))
    flow_entries.append(wh.FlowEntry(symptom_disease_annotator))
    flow_entries.append(wh.FlowEntry(toileting_annotator))
    flow_entries.append(wh.FlowEntry(walking_annotator))
    flow_entries.append(wh.FlowEntry(section))

    flow = wh.Flow(flow_entries, False)
    annotator_flow = wh.AnnotatorFlow(flow=flow)

    containers = [wh.UnstructuredContainer(text=TEXT)]
    flows = [annotator_flow]

    response = ACD.analyze_org(containers, flows)
    container_group = wh.ContainerGroup._from_dict(response.get_result())

    for unstructured_container in container_group.unstructured:
        if unstructured_container.text is not None:
            assert unstructured_container.text == TEXT
        if unstructured_container.id is not None:
            assert unstructured_container.id != '0'
        if unstructured_container.type is not None:
            assert unstructured_container.type != 'bogus'
        
        assert unstructured_container.data is not None
        tuc.TestUnstructuredContainer.test_unstructured_container(data=unstructured_container.data)

def test_analyze():

    config_entry = wh.ConfigurationEntity(id='test', type='test', uid=99)
    configs = [config_entry]

    allergy_annotator = wh.Annotator(name=wh.Name.ALLERGY)
    attr_detect_annotator = wh.Annotator(name=wh.Name.ATTRIBUTE_DETECTION)
    bathing_annotator = wh.Annotator(name=wh.Name.BATHING_ASSISTANCE)
    cancer_annotator = wh.Annotator(name=wh.Name.CANCER)
    concept_detect_annotator = wh.Annotator(name=wh.Name.CONCEPT_DETECTION)
    disambig_annotator = wh.Annotator(name=wh.Name.DISAMBIGUATION)
    dressing_annotator = wh.Annotator(name=wh.Name.DRESSING_ASSISTANCE)
    eating_annotator = wh.Annotator(name=wh.Name.EATING_ASSISTANCE)
    ef_annotator = wh.Annotator(name=wh.Name.EJECTION_FRACTION)
    hypothetical_annotator = wh.Annotator(name=wh.Name.HYPOTHETICAL)
    lab_value_annotator = wh.Annotator(name=wh.Name.LAB_VALUE)
    medication_annotator = wh.Annotator(name=wh.Name.MEDICATION)
    named_entities_annotator = wh.Annotator(name=wh.Name.NAMED_ENTITIES)
    negation_annotator = wh.Annotator(name=wh.Name.NEGATION)
    procedure_annotator = wh.Annotator(name=wh.Name.PROCEDURE)
    seeing_annotator = wh.Annotator(name=wh.Name.SEEING_ASSISTANCE)
    smoking_annotator = wh.Annotator(name=wh.Name.SMOKING)
    spelling_annotator = wh.Annotator(name=wh.Name.SPELL_CHECKER)
    symptom_disease_annotator = wh.Annotator(name=wh.Name.SYMPTOM_DISEASE)
    toileting_annotator = wh.Annotator(name=wh.Name.TOILETING_ASSISTANCE)
    walking_annotator = wh.Annotator(name=wh.Name.WALKING_ASSISTANCE)
    section = wh.Annotator(name=wh.Name.SECTION)

    flow_entries = []
    flow_entries.append(wh.FlowEntry(allergy_annotator))
    flow_entries.append(wh.FlowEntry(attr_detect_annotator))
    flow_entries.append(wh.FlowEntry(bathing_annotator))
    flow_entries.append(wh.FlowEntry(cancer_annotator))
    flow_entries.append(wh.FlowEntry(concept_detect_annotator))
    flow_entries.append(wh.FlowEntry(disambig_annotator))
    flow_entries.append(wh.FlowEntry(dressing_annotator))
    flow_entries.append(wh.FlowEntry(eating_annotator))
    flow_entries.append(wh.FlowEntry(ef_annotator))
    flow_entries.append(wh.FlowEntry(hypothetical_annotator))
    flow_entries.append(wh.FlowEntry(lab_value_annotator))
    flow_entries.append(wh.FlowEntry(medication_annotator))
    flow_entries.append(wh.FlowEntry(named_entities_annotator))
#    flow_entries.append(wh.FlowEntry(negation_annotator))
    flow_entries.append(wh.FlowEntry(procedure_annotator))
    flow_entries.append(wh.FlowEntry(seeing_annotator))
    flow_entries.append(wh.FlowEntry(smoking_annotator))
    flow_entries.append(wh.FlowEntry(spelling_annotator))
    flow_entries.append(wh.FlowEntry(symptom_disease_annotator))
    flow_entries.append(wh.FlowEntry(toileting_annotator))
    flow_entries.append(wh.FlowEntry(walking_annotator))
    flow_entries.append(wh.FlowEntry(section))

    flow = wh.Flow(flow_entries, False)
    annotator_flow = wh.AnnotatorFlow(flow)

    containers = [wh.UnstructuredContainer(text=TEXT)]

    data = ACD.analyze(TEXT, flow)
    tuc.TestUnstructuredContainer.test_unstructured_container(data=data)

def test_analyze_text_array():

    config_entry = wh.ConfigurationEntity(id='test', type='test', uid=99)
    configs = [config_entry]

    allergy_annotator = wh.Annotator(name=wh.Name.ALLERGY)
    attr_detect_annotator = wh.Annotator(name=wh.Name.ATTRIBUTE_DETECTION)
    bathing_annotator = wh.Annotator(name=wh.Name.BATHING_ASSISTANCE)
    cancer_annotator = wh.Annotator(name=wh.Name.CANCER)
    concept_detect_annotator = wh.Annotator(name=wh.Name.CONCEPT_DETECTION)
    disambig_annotator = wh.Annotator(name=wh.Name.DISAMBIGUATION)
    dressing_annotator = wh.Annotator(name=wh.Name.DRESSING_ASSISTANCE)
    eating_annotator = wh.Annotator(name=wh.Name.EATING_ASSISTANCE)
    ef_annotator = wh.Annotator(name=wh.Name.EJECTION_FRACTION)
    hypothetical_annotator = wh.Annotator(name=wh.Name.HYPOTHETICAL)
    lab_value_annotator = wh.Annotator(name=wh.Name.LAB_VALUE)
    medication_annotator = wh.Annotator(name=wh.Name.MEDICATION)
    named_entities_annotator = wh.Annotator(name=wh.Name.NAMED_ENTITIES)
    negation_annotator = wh.Annotator(name=wh.Name.NEGATION)
    procedure_annotator = wh.Annotator(name=wh.Name.PROCEDURE)
    seeing_annotator = wh.Annotator(name=wh.Name.SEEING_ASSISTANCE)
    smoking_annotator = wh.Annotator(name=wh.Name.SMOKING)
    spelling_annotator = wh.Annotator(name=wh.Name.SPELL_CHECKER)
    symptom_disease_annotator = wh.Annotator(name=wh.Name.SYMPTOM_DISEASE)
    toileting_annotator = wh.Annotator(name=wh.Name.TOILETING_ASSISTANCE)
    walking_annotator = wh.Annotator(name=wh.Name.WALKING_ASSISTANCE)
    section = wh.Annotator(name=wh.Name.SECTION)

    flow_entries = []
    flow_entries.append(wh.FlowEntry(allergy_annotator))
    flow_entries.append(wh.FlowEntry(attr_detect_annotator))
    flow_entries.append(wh.FlowEntry(bathing_annotator))
    flow_entries.append(wh.FlowEntry(cancer_annotator))
    flow_entries.append(wh.FlowEntry(concept_detect_annotator))
    flow_entries.append(wh.FlowEntry(disambig_annotator))
    flow_entries.append(wh.FlowEntry(dressing_annotator))
    flow_entries.append(wh.FlowEntry(eating_annotator))
    flow_entries.append(wh.FlowEntry(ef_annotator))
    flow_entries.append(wh.FlowEntry(hypothetical_annotator))
    flow_entries.append(wh.FlowEntry(lab_value_annotator))
    flow_entries.append(wh.FlowEntry(medication_annotator))
    flow_entries.append(wh.FlowEntry(named_entities_annotator))
#    flow_entries.append(wh.FlowEntry(negation_annotator))
    flow_entries.append(wh.FlowEntry(procedure_annotator))
    flow_entries.append(wh.FlowEntry(seeing_annotator))
    flow_entries.append(wh.FlowEntry(smoking_annotator))
    flow_entries.append(wh.FlowEntry(spelling_annotator))
    flow_entries.append(wh.FlowEntry(symptom_disease_annotator))
    flow_entries.append(wh.FlowEntry(toileting_annotator))
    flow_entries.append(wh.FlowEntry(walking_annotator))
    flow_entries.append(wh.FlowEntry(section))

    flow = wh.Flow(flow_entries, False)
    annotator_flow = wh.AnnotatorFlow(flow)

    containers = [wh.UnstructuredContainer(text=TEXT)]

    container_group = ACD.analyze([TEXT], flow)

    for unstructured_container in container_group.unstructured:
        if unstructured_container.text is not None:
            assert unstructured_container.text == TEXT
        if unstructured_container.id is not None:
            assert unstructured_container.id != '0'
        if unstructured_container.type is not None:
            assert unstructured_container.type != 'bogus'
        
        assert unstructured_container.data is not None
        tuc.TestUnstructuredContainer.test_unstructured_container(data=unstructured_container.data)
