from collections import defaultdict
from gym.envs.toy_text import BlackjackEnv
from blackjack.common import DeterministicPolicy, StateValue, gen_episode_data, fixed_policy
from blackjack.plotting import plot_value_function


def mc_prediction_every_visit(policy: DeterministicPolicy, env: BlackjackEnv,
                              num_episodes, discount_factor=1.0) -> StateValue:
    returns_sum = defaultdict(float)
    returns_count = defaultdict(float)

    for episode_i in range(1, num_episodes + 1):
        episode_history = gen_episode_data(policy, env)

        G = 0
        for t in range(len(episode_history) - 1, -1, -1):
            s, a, r = episode_history[t]
            G = discount_factor * G + r
            returns_sum[s] += G
            returns_count[s] += 1.0

    V = defaultdict(float)
    V.update({s: returns_sum[s] / returns_count[s] for s in returns_sum.keys()})
    return V


if __name__ == "__main__":
    env = BlackjackEnv()

    num_episodes = 10000
    V = mc_prediction_every_visit(fixed_policy, env, num_episodes=num_episodes)

    plot_value_function(V, title=f'Every Visit {num_episodes} Steps')

    # V_500k = mc_prediction(sample_policy, env, num_episodes=50000)
    # plotting.plot_value_function(V_500k, title="500,000 Steps")
