from src.evaluation.evaluator_manager import EvaluatorManager
import sys

import wandb
import numpy as np 
import random


config_file_path = sys.argv[1]
runno = int(sys.argv[2])

print('Executing:'+sys.argv[1])

# Define sweep config
sweep_configuration = {
    'method': 'grid',
    'name': f'GCounteRGAN_Runno={runno}',
    'metric': {'goal': 'maximize', 'name': 'Correctness'},
    'parameters': 
    {
        'training_iterations': {'values': list(range(10, 101, 10))},
        'sampling_iterations': {'values': list(range(10, 101, 10))},
        'lr_generator': {'values': [1e-4, 1e-3, 1e-2]},
        'lr_discriminator': {'values': [1e-4, 1e-3, 1e-2]}
     }
}

print('Creating the evaluation manager.......................................................')
eval_manager = EvaluatorManager(config_file_path, run_number=runno)

# Initialize sweep by passing in config. 
sweep_id = wandb.sweep(
  sweep=sweep_configuration, 
  project='GRETEL'
)

# sweep through the folds
def main():
    metric_reports = None

    for fold_id in range(5):
        run = wandb.init()
        # note that we define values from `wandb.config`  
        # instead of defining hard values
        lr_generator  =  wandb.config.lr_generator
        lr_discriminator = wandb.config.lr_discriminator
        training_iterations = wandb.config.training_iterations
        sampling_iterations = wandb.config.sampling_iterations
    
        print('Creating the evaluators...................................................................')
        eval_manager.create_evaluators()
        eval_manager.explainers[0].fold_id = fold_id
        eval_manager.explainers[0].lr_generator = lr_generator
        eval_manager.explainers[0].lr_discriminator = lr_discriminator
        eval_manager.explainers[0].training_iterations = training_iterations
        eval_manager.explainers[0].sampling_iterations = sampling_iterations
        
        print('Evaluating the explainers..................................................................')
        eval_manager.evaluate()

        if metric_reports is None:
            # The metrics are not available in the evaluator manager until we create the evaluators
            metric_reports = {f'{metric.name}': [] for metric in eval_manager.evaluation_metrics}
        
        for evaluator in eval_manager.evaluators:
            for metric in eval_manager.evaluation_metrics:
                metric_reports[f'{metric.name}'].append(evaluator._results[f'{metric.name}'])

    wandb.log({
        f'{metric.name}': np.mean(metric_reports[f'{metric.name}']) for metric in eval_manager.evaluation_metrics
    })

# Start the sweep job
wandb.agent(sweep_id, function=main, count=5)
