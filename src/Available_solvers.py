# Licensing Information:  You are free to use or extend this codebase for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) inform Guni Sharon at 
# guni@tamu.edu regarding your usage (relevant statistics is reported to NSF).
# The development of this assignment was supported by NSF (IIS-2238979).
# Contributors:
# The core code base was developed by Guni Sharon (guni@tamu.edu).

solvers = [
    "random",
    "vi",
    "pi",
    "mc",
    "avi",
    "mcis",
    "ql",
    "sarsa",
    "aql",
    "dqn",
    "reinforce",
    "a2c",
    "ddpg",
    "ppo",
]


def get_solver_class(name):
    if name == solvers[0]:
        from .Random_Walk import RandomWalk

        return RandomWalk
    elif name == solvers[1]:
        from .Value_Iteration import ValueIteration

        return ValueIteration
    elif name == solvers[2]:
        from .Policy_Iteration import PolicyIteration

        return PolicyIteration
    elif name == solvers[3]:
        from .Monte_Carlo import MonteCarlo

        return MonteCarlo
    elif name == solvers[4]:
        from .Value_Iteration import AsynchVI

        return AsynchVI
    elif name == solvers[5]:
        from .Monte_Carlo import OffPolicyMC

        return OffPolicyMC
    elif name == solvers[6]:
        from .Q_Learning import QLearning

        return QLearning
    elif name == solvers[7]:
        from .SARSA import Sarsa

        return Sarsa
    elif name == solvers[8]:
        from .Q_Learning import ApproxQLearning

        return ApproxQLearning
    elif name == solvers[9]:
        from .DQN import DQN

        return DQN
    elif name == solvers[10]:
        from .REINFORCE import Reinforce

        return Reinforce
    elif name == solvers[11]:
        from .A2C import A2C

        return A2C
    elif name == solvers[12]:
        from .DDPG import DDPG

        return DDPG
    elif name == solvers[13]:
        from .PPO import PPO

        return PPO
    else:
        assert False, "unknown solver name {}. solver must be from {}".format(
            name, str(solvers)
        )
