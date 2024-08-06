import importlib.util
import os
import pygame
import numpy as np
import signal
import sys
from glob import glob
from tqdm import tqdm
from env_design.wrapped_envs.pomdp_gym import PygameEnv
from env_design.wrapped_envs.oop_gym import PygameOOPEnv


def env_creator(env_config):
    env_list = []
    env_name = env_config["name"]

    if env_config["method"] == "ours":
        version, numbered_directory = env_config['version'].split('_')
        directory_path = f"env_design/generated_envs/{env_name}_eval/{version}/"
        for filename in os.listdir(directory_path):
            # Load the module from the file
            if filename.startswith('pomdp'):
                # Construct a full file path
                file_path = directory_path + '/' + filename + f'/{numbered_directory}/' + 'final.py'
                # Define module name based on file name and load the Game module from the file
                module_name = filename
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    env_list.append((module_name, getattr(module, f"Game")))
                except Exception as e:
                    print(f"Fail to load {module_name}")

        env_config["env_list"] = sorted(env_list)
        env = PygameEnv(env_config)
        return env

    elif env_config["method"] == "baseline":
        version  = env_config['version']
        directory_path = f"env_design/generated_envs/{env_name}_baseline_eval/{version}"
        for filename in os.listdir(directory_path):
            # Load the module from the file
            if filename.endswith(".py"):
                # Construct a full file path
                file_path = directory_path + '/' + filename
                # Define module name based on file name and load the Game module from the file
                module_name = filename
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    env_list.append((module_name, getattr(module, f"Game")))
                except Exception as e:
                    print(f"Fail to load {module_name}")

        env_config["env_list"] = sorted(env_list)
        env = PygameOOPEnv(env_config)
        return env
            
    else:
        assert False

def get_env_list(env_config):
    env_list = []
    env_name = env_config["name"]

    if env_config["method"] == "ours":
        version, numbered_directory = env_config['version'].split('_')
        directory_path = f"env_design/generated_envs/{env_name}_eval/{version}/"
        for filename in os.listdir(directory_path):
            # Load the module from the file
            if filename.startswith('pomdp'):
                # Construct a full file path
                file_path = directory_path + '/' + filename + f'/{numbered_directory}/' + 'final.py'
                # Define module name based on file name and load the Game module from the file
                module_name = filename
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    env_list.append((module_name, getattr(module, f"Game")))
                except Exception as e:
                    print(f"Fail to load {module_name}")

        env_config["env_list"] = sorted(env_list)
        return env_config["env_list"]
        #env = PygameEnv(env_config)
        #return env

    elif env_config["method"] == "baseline":
        version  = env_config['version']
        directory_path = f"env_design/generated_envs/{env_name}_baseline_eval/{version}"
        for filename in os.listdir(directory_path):
            # Load the module from the file
            if filename.endswith(".py"):
                # Construct a full file path
                file_path = directory_path + '/' + filename
                # Define module name based on file name and load the Game module from the file
                module_name = filename
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    env_list.append((module_name, getattr(module, f"Game")))
                except Exception as e:
                    print(f"Fail to load {module_name}")

        env_config["env_list"] = sorted(env_list)
        return env_config["env_list"]
        #env = PygameOOPEnv(env_config)
        #return env
            
    else:
        assert False


def my_env_check(env):
    total_rewards = []
    for _ in range(5):
        print('start evaluating ...')
        try:
            observation, _ = env.reset()
            done = False
            total_reward = 0
            idx = 0
            for i in tqdm(range(500)):
                action = env.action_space.sample()
                observation, reward, done, truncated, info = env.step(action)
                if info["has_exception"]:
                    return False
                total_reward += reward
                if done:
                    break
            total_rewards.append(total_reward)
            print(f"total reward: {total_reward}")
            pygame.quit()
            env.close()
        except Exception as e:
            print(e)
            return False

    print(total_rewards)
    if env.env_name == "pong":
        # check if all the values are the same
        if np.all([total_rewards[i] == total_rewards[0] for i in range(len(total_rewards))]):
            return False
        if np.sum(total_rewards) == 0:
            return False
    return True


if __name__ == '__main__':
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    #game = "flappy_bird"
    #game = "catcher"
    game = sys.argv[1]
    version = sys.argv[2]
    try:
        method = sys.argv[3]
    except IndexError:
        print("using default method: ours")
        method = "ours"
    #version = "v8_4"
    #for method in ["one_shot", "debug", "sequential", "ours"]:

    if method == "ours":
        directory_path = f"env_design/generated_envs/{game}_eval/{version.split('_')[0]}"
        env_config = {"name": game, "method": method, "version": version, "max_episode_steps": 10000}
        env_list = get_env_list(env_config)
        print('num_folders', len(env_list))

        failed_env_list = []
        for selected_env_id, env_class in env_list:
            env_config["env_id"] = selected_env_id
            env_config["env_class"] = env_class
            print(selected_env_id)
            try:
                env = PygameEnv(env_config)
                if not my_env_check(env):
                    failed_env_list.append(selected_env_id)
            except Exception as e:
                print(e)
                failed_env_list.append(selected_env_id)

    elif method == "baseline":
        directory_path = f"env_design/generated_envs/{game}_baseline_eval/{version}"
        env_config = {"name": game, "method": method, "version": version, "max_episode_steps": 10000}
        env_list = get_env_list(env_config)
        print('num_folders', len(env_list))

        failed_env_list = []
        for selected_env_id, env_class in env_list:
            env_config["env_id"] = selected_env_id
            env_config["env_class"] = env_class
            print(selected_env_id)
            try:
                env = PygameOOPEnv(env_config)
                if not my_env_check(env):
                    failed_env_list.append(selected_env_id)
            except Exception as e:
                print('===================', e)
                failed_env_list.append(selected_env_id)

    print(failed_env_list)
    for selected_env_id in failed_env_list:
        # move the folder {directory_path}/{env.selected_env_name} to {directory_path}/unverified
        print(f"moving the folder {directory_path}/{selected_env_id} to {directory_path}/unverified")
        os.makedirs(directory_path + "/unverified", exist_ok=True)
        os.rename(directory_path + "/" + selected_env_id, directory_path + "/unverified/" + selected_env_id)
        pygame.quit()
        continue