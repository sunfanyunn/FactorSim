# FactorSim

### Simulation Generation
Refer to the README under the directory `factorsim`.
```
$ cd factorsim
$ ./go.sh GAME_NAME
```

### Zero-shot transfer experiments 
Refer to [rl_training/rl_train.sh]

To train RL policies on the ``ground-truth'' PLE environments, run 
```
$ cd rl_training
$ ./rl_train.sh pong ppo gt --train_on_ple
```

To train RL policies on the generated environments, run:
TODO

### Miscellaneous
To export video trajectory of a policy, run 
`python -m utils.export_video pong`


## Acknowledgement
- [PLE: A Reinforcement Learning Environment](https://pygame-learning-environment.readthedocs.io/en/latest/)
- [RLLib](https://docs.ray.io/en/latest/rllib/index.html)