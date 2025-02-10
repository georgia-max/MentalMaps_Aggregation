import os
import json
import pandas as pd

from datetime import datetime


def save_run_results(dataset_path, pretrained_model, dataset_shape, result, result_path, trainer, model, hyperparams=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # set the path to models\fine_tune_model

    run_dir = os.path.join(result_path, f'run_{timestamp}')
    os.makedirs(run_dir, exist_ok=True)

    # Save model
    model.save_pretrained(os.path.join(run_dir, 'model'))

    summary = {
        'dataset': dataset_path,
        'pretrained_model': pretrained_model,
        'dataset_shape': dataset_shape,
        'results': result
    }

    # Save metrics and hyperparameters
    with open(os.path.join(run_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f)
    if hyperparams is not None:
        with open(os.path.join(run_dir, 'hyperparams.json'), 'w') as f:
            json.dump(hyperparams, f)

    # save trainer
    trainer.save_model(run_dir)
