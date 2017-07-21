# -*- coding: utf-8 -*-
"""
    ptutils.constants
    ~~~~~~~~~~~~~~~~~

    This module defines core ptutils constants.
"""
import yaml
import json
import cPickle as pickle
from collections import OrderedDict


CONFIG_TYPES = {'yml': {'file': yaml.load, 'data': yaml.load},
                'yaml': {'file': yaml.load, 'data': yaml.load},
                'json': {'file': json.load, 'data': json.loads},
                'pkl': {'file': pickle.load, 'data': pickle.loads}}

# BASE_MODULE = {
#     'NAME': {
#         'STATE': 'State',
#         'MODEL': 'Model',
#         'MODULE': 'Module',
#         'RUNNER': 'Runner',
#         'STATUS': 'Status',
#         'TESTER': 'Tester',
#         'DATASET': 'Dataset',
#         'MONITOR': 'Monitor',
#         'SAMPLER': 'Sampler',
#         'SESSION': 'Session',
#         'TRAINER': 'Trainer',
#         'CRITERION': 'Criterion',
#         'OPTIMIZER': 'Optimizer',
#         'DATALOADER': 'Dataloader',
#         'DATAREADER': 'Datareader',
#         'DBINTERFACE': 'DBInterface',
#         'DATAPROVIDER': 'Dataprovider',
#         'CONFIGURATION': 'Configuration',
#     },
# }
# BASE_MODULE['BASES'] = {
#     'MODEL': ('ptutils.base.Module',),
#     'MODULE': ('ptutils.base.Module',),
#     'RUNNER': ('ptutils.base.Module',),
#     'TESTER': ('ptutils.base.Module',),
#     'DATASET': ('ptutils.base.Module',),
#     'MONITOR': ('ptutils.base.Module',),
#     'SAMPLER': ('ptutils.base.Module',),
#     'SESSION': ('ptutils.base.Module',),
#     'TRAINER': ('ptutils.base.Module',),
#     'CRITERION': ('ptutils.base.Module',),
#     'OPTIMIZER': ('ptutils.base.Module',),
#     'DATALOADER': ('ptutils.base.Module',),
#     'DATAREADER': ('ptutils.base.Module',),
#     'DBINTERFACE': ('ptutils.base.Module',),
#     'DATAPROVIDER': ('ptutils.base.Module',),
# }

# BASE_MODULE['DICT'] = {
#     'MODEL': {'__base__': BASE_MODULE['NAME']['MODEL'],
#               '__name__': BASE_MODULE['NAME']['MODEL'].lower()},
#     'STATE': {'__base__': BASE_MODULE['NAME']['STATE'],
#               '__name__': BASE_MODULE['NAME']['STATE'].lower()},
#     'MODULE': {'__base__': BASE_MODULE['NAME']['MODULE'],
#                '__name__': BASE_MODULE['NAME']['MODULE'].lower()},
#     'RUNNER': {'__base__': BASE_MODULE['NAME']['RUNNER'],
#                '__name__': BASE_MODULE['NAME']['RUNNER'].lower()},
#     'STATUS': {'__base__': BASE_MODULE['NAME']['STATUS'],
#                '__name__': BASE_MODULE['NAME']['STATUS'].lower()},
#     'TESTER': {'__base__': BASE_MODULE['NAME']['TESTER'],
#                '__name__': BASE_MODULE['NAME']['TESTER'].lower()},
#     'DATASET': {'__base__': BASE_MODULE['NAME']['DATASET'],
#                 '__name__': BASE_MODULE['NAME']['DATASET'].lower()},
#     'MONITOR': {'__base__': BASE_MODULE['NAME']['MONITOR'],
#                 '__name__': BASE_MODULE['NAME']['MONITOR'].lower()},
#     'SAMPLER': {'__base__': BASE_MODULE['NAME']['SAMPLER'],
#                 '__name__': BASE_MODULE['NAME']['SAMPLER'].lower()},
#     'SESSION': {'__base__': BASE_MODULE['NAME']['SESSION'],
#                 '__name__': BASE_MODULE['NAME']['SESSION'].lower()},
#     'TRAINER': {'__base__': BASE_MODULE['NAME']['TRAINER'],
#                 '__name__': BASE_MODULE['NAME']['TRAINER'].lower()},
#     'CRITERION': {'__base__': BASE_MODULE['NAME']['CRITERION'],
#                   '__name__': BASE_MODULE['NAME']['CRITERION'].lower()},
#     'OPTIMIZER': {'__base__': BASE_MODULE['NAME']['OPTIMIZER'],
#                   '__name__': BASE_MODULE['NAME']['OPTIMIZER'].lower()},
#     'DATALOADER': {'__base__': BASE_MODULE['NAME']['DATALOADER'],
#                    '__name__': BASE_MODULE['NAME']['DATALOADER'].lower()},
#     'DATAREADER': {'__base__': BASE_MODULE['NAME']['DATAREADER'],
#                    '__name__': BASE_MODULE['NAME']['DATAREADER'].lower()},
#     'DBINTERFACE': {'__base__': BASE_MODULE['NAME']['DBINTERFACE'],
#                     '__name__': BASE_MODULE['NAME']['DBINTERFACE'].lower()},
#     'DATAPROVIDER': {'__base__': BASE_MODULE['NAME']['DATAPROVIDER'],
#                      '__name__': BASE_MODULE['NAME']['DATAPROVIDER'].lower()},
#     'CONFIGURATION': {'__base__': BASE_MODULE['NAME']['CONFIGURATION'],
#                       '__name__': BASE_MODULE['NAME']['CONFIGURATION'].lower()},
# }

BASE = {
    'STATE': OrderedDict([
        ('NAME', 'State'),
        ('BASES', ('ptutils.module.State',)),
        ('DICT', {}),
    ]),
    'MODULE': OrderedDict([
        ('NAME', 'Module'),
        ('BASES', ('ptutils.module.Module',)),
        ('DICT', {}),
    ]),
    'MODEL': OrderedDict([
        ('NAME', 'Model'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'PLUGIN': OrderedDict([
        ('NAME', 'Plugin'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'RUNNER': OrderedDict([
        ('NAME', 'Runner'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'STATUS': OrderedDict([
        ('NAME', 'Status'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'TESTER': OrderedDict([
        ('NAME', 'Tester'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'DATASET': OrderedDict([
        ('NAME', 'Dataset'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),

    'SAMPLER': OrderedDict([
        ('NAME', 'Sampler'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'SESSION': OrderedDict([
        ('NAME', 'Session'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'TRAINER': OrderedDict([
        ('NAME', 'Trainer'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'CRITERION': OrderedDict([
        ('NAME', 'Criterion'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'OPTIMIZER': OrderedDict([
        ('NAME', 'Optimizer'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'DATALOADER': OrderedDict([
        ('NAME', 'DataLoader'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'DATAREADER': OrderedDict([
        ('NAME', 'DataReader'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'DBINTERFACE': OrderedDict([
        ('NAME', 'DBInterface'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'DATABASE': OrderedDict([
        ('NAME', 'DATABASE'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'DATAPROVIDER': OrderedDict([
        ('NAME', 'DataProvider'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
    'CONFIGURATION': OrderedDict([
        ('NAME', 'Configuration'),
        ('BASES', ('ptutils.base.Module',)),
        ('DICT', {}),
    ]),
}


# STATE_BASES = (State,)
# STATUS_BASES = (Module, Status)
# CONFIGURATION_BASES = (Module, Configuration)
# # State = type(STATE_NAME, STATE_BASES, STATE_DICT)
# # Module = type(MODULE_NAME, MODULE_BASES, MODULE_DICT)

# # MODULE TYPE
# Model = type(MODEL_NAME, MODEL_BASES, MODEL_DICT)
# Runner = type(RUNNER_NAME, RUNNER_BASES, RUNNER_DICT)
# Status = type(STATUS_NAME, STATUS_BASES, STATUS_DICT)
# Tester = type(TESTER_NAME, TESTER_BASES, TESTER_DICT)
# DataSet = type(DATASET_NAME, DATASET_BASES, DATASET_DICT)
# Monitor = type(MONITOR_NAME, MONITOR_BASES, MONITOR_DICT)
# Sampler = type(SAMPLER_NAME, SAMPLER_BASES, SAMPLER_DICT)
# Session = type(SESSION_NAME, SESSION_BASES, SESSION_DICT)
# Trainer = type(TRAINER_NAME, TRAINER_BASES, TRAINER_DICT)
# Criterion = type(CRITERION_NAME, CRITERION_BASES, CRITERION_DICT)
# Optimizer = type(OPTIMIZER_NAME, OPTIMIZER_BASES, OPTIMIZER_DICT)
# Dataloader = type(DATALOADER_NAME, DATALOADER_BASES, DATALOADER_DICT)
# DataReader = type(DATAREADER_NAME, DATAREADER_BASES, DATAREADER_DICT)
# DBInterface = type(DBINTERFACE_NAME, DBINTERFACE_BASES, DBINTERFACE_DICT)
# DataProvider = type(DATAPROVIDER_NAME, DATAPROVIDER_BASES, DATAPROVIDER_DICT)
# Configuration = type(CONFIGURATION_NAME, CONFIGURATION_BASES,
# CONFIGURATION_DICT)

# BASE_MODULES = {
#     MODEL_NAME: Model,
#     STATE_NAME: State,
#     MODULE_NAME: Module,
#     RUNNER_NAME: Runner,
#     STATUS_NAME: Status,
#     TESTER_NAME: Tester,
#     DATASET_NAME: DataSet,
#     MONITOR_NAME: Monitor,
#     SAMPLER_NAME: Sampler,
#     SESSION_NAME: Session,
#     TRAINER_NAME: Trainer,
#     CRITERION_NAME: Criterion,
#     OPTIMIZER_NAME: Optimizer,
#     DATALOADER_NAME: Dataloader,
#     DATAREADER_NAME: DataReader,
#     DBINTERFACE_NAME: DBInterface,
#     DATAPROVIDER_NAME: DataProvider,
#     CONFIGURATION_NAME: Configuration,
# }

# BASE_TYPES = {
#     Model: MODEL_NAME,
#     State: STATE_NAME,
#     Module: MODULE_NAME,
#     Runner: RUNNER_NAME,
#     Status: STATUS_NAME,
#     Tester: TESTER_NAME,
#     DataSet: DATASET_NAME,
#     Monitor: MONITOR_NAME,
#     Sampler: SAMPLER_NAME,
#     Session: SESSION_NAME,
#     Trainer: TRAINER_NAME,
#     Criterion: CRITERION_NAME,
#     Optimizer: OPTIMIZER_NAME,
#     Dataloader: DATALOADER_NAME,
#     DataReader: DATAREADER_NAME,
#     DBInterface: DBINTERFACE_NAME,
#     DataProvider: DATAPROVIDER_NAME,
#     Configuration: CONFIGURATION_NAME,
# }

# CORE_MODULES = {
#     MODEL_NAME: Model,
#     STATE_NAME: State,
#     DBINTERFACE_NAME: DBInterface,
#     DBINTERFACE_NAME: DataProvider,
#     CONFIGURATION_NAME: Configuration,
# }

# AUX_MODULES = {
#     STATUS_NAME: Status,
#     CRITERION_NAME: Criterion,
#     OPTIMIZER_NAME: Optimizer,
# }

# _CORE_MODULES = {
#     Model.__dict__.get('__name__', Model.__name__): Model,
#     DBInterface.__dict__.get('__name__', DBInterface.__name__): DBInterface,
#     DataProvider.__dict__.get('__name__', DataProvider.__name__): DataProvider,
# }

# BASE_MODULES = {
#     Model.__dict__.get('__name__', Model.__name__): Model,
#     DBInterface.__dict__.get('__name__', DBInterface.__name__): DBInterface,
#     DataProvider.__dict__.get('__name__', DataProvider.__name__): DataProvider,
# }
