# FactorSim

### Environment Usage

To export video trajectory of a policy, run 
`python -m utils.export_video pong`

### Generating RL Environments

refer to https://github.com/sunfanyunn/FactorSim/tree/master/LLM-POMDP

### Training RL policies

To train RL policies on the ``ground-truth'' PLE environments, run 
`./rl_train.sh pong ppo gt --train_on_ple`

To train RL policies on the generated environments, run
`

## Acknowledgement

- [PLE: A Reinforcement Learning Environment](https://pygame-learning-environment.readthedocs.io/en/latest/)


