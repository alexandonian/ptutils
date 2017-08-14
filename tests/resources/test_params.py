"""tfutils style params dictionary for testing.

Attributes:
    params (dict): Params for train_from_params.

"""
params = {}
params['model_params'] = {'func': 'model.mnist_tfutils'}
params['save_params'] = {'host': 'testhost',
                         'port': 'testport',
                         'dbname': 'testdbname',
                         'collname': 'testcol',
                         'exp_id': 'training0',
                         'save_valid_freq': 20,
                         'save_filters_freq': 200,
                         'cache_filters_freq': 100}
params['train_params'] = {'data_params': {'func': 'data.MNIST',
                                          'batch_size': 100,
                                          'group': 'train',
                                          'n_threads': 4},
                           'queue_params': {'queue_type': 'fifo',
                                            'batch_size': 100},
                            'num_steps': 500}
params['learning_rate_params'] = {'learning_rate': 0.05,
                                  'decay_steps': 'num_batches_per_epoch',
                                  'decay_rate': 0.95,
                                  'staircase': True}
params['validation_params'] = {'valid0': {'data_params': {'func': 'data.MNIST',
                                                          'batch_size': 100,
                                                          'group': 'test',
                                                          'n_threads': 4},
                                          'queue_params': {'queue_type': 'fifo',
                                                           'batch_size': 100},
                                          'num_steps': 100,
                                          'agg_func': 'utils.mean_dict'}}
params['skip_check'] = True
