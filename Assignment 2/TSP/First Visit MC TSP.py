from typing import Dict, List, Optional, Tuple
import gymnasium as gym
import numpy as np


class TSP(gym.Env):
    """Traveling Salesman Problem (TSP) RL environment for persistent monitoring."""

    def __init__(self, num_targets: int, max_area: int = 30, seed: int = None) -> None:
        super().__init__()
        if seed is not None:
            np.random.seed(seed=seed)

        self.steps: int = 0
        self.num_targets: int = num_targets
        self.max_steps: int = num_targets
        self.max_area: int = max_area

        self.locations: np.ndarray = self._generate_points(self.num_targets)
        self.distances: np.ndarray = self._calculate_distances(self.locations)

        self.obs_low = self._build_obs_low()
        self.obs_high = self._build_obs_high()

        self.observation_space = gym.spaces.Box(low=self.obs_low, high=self.obs_high)
        self.action_space = gym.spaces.Discrete(self.num_targets)

    def _build_obs_low(self) -> np.ndarray:
        return np.concatenate(
            [
                np.array([0], dtype=np.float32),
                np.zeros(self.num_targets, dtype=np.float32),
                np.zeros(2 * self.num_targets, dtype=np.float32),
            ]
        )

    def _build_obs_high(self) -> np.ndarray:
        return np.concatenate(
            [
                np.array([self.num_targets], dtype=np.float32),
                2 * self.max_area * np.ones(self.num_targets, dtype=np.float32),
                self.max_area * np.ones(2 * self.num_targets, dtype=np.float32),
            ]
        )

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
        init_loc: Optional[int] = 0,
    ) -> Tuple[np.ndarray, Dict[str, None]]:
        self.steps = 0
        self.loc = init_loc
        self.visited_targets = []
        self.dist = self.distances[self.loc]

        state = self._get_state()
        return state, {}

    def _get_state(self) -> np.ndarray:
        return np.concatenate(
            (
                np.array([self.loc]),
                np.array(self.dist),
                np.array(self.locations).reshape(-1),
            ),
            dtype=np.float32,
        )

    def step(
        self, action: int
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, None]]:
        self.steps += 1
        past_loc = self.loc
        next_loc = action

        reward = self._get_rewards(past_loc, next_loc)
        self.visited_targets.append(next_loc)

        self.loc, self.dist = next_loc, self.distances[next_loc]
        terminated = self.steps == self.max_steps
        truncated = False

        next_state = self._get_state()
        return next_state, reward, terminated, truncated, {}

    def _generate_points(self, num_points: int) -> np.ndarray:
        points = []
        while len(points) < num_points:
            x, y = np.random.random() * self.max_area, np.random.random() * self.max_area
            if [x, y] not in points:
                points.append([x, y])
        return np.array(points)

    def _calculate_distances(self, locations: List) -> np.ndarray:
        n = len(locations)
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                distances[i, j] = np.linalg.norm(locations[i] - locations[j])
        return distances

    def _get_rewards(self, past_loc: int, next_loc: int) -> float:
        if next_loc not in self.visited_targets:
            return -self.distances[past_loc][next_loc]
        return -10000  # Penalize revisits


def train_tsp(env: TSP, max_episodes: int, max_steps: int, gamma: float) -> Tuple[Dict, List[float]]:
    policy, Qvalue, Returns = {}, {}, {}
    ep_rets = []

    for ep in range(max_episodes):
        obs, _ = env.reset(init_loc=env.action_space.sample())
        action = env.action_space.sample()
        episode = []

        for step in range(max_steps):
            next_obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            episode.append((obs, action, reward))

            obs = next_obs
            action = policy.get(env.loc, env.action_space.sample())

            if done:
                break

        G = update_policy(episode, gamma, policy, Qvalue, Returns, env)
        ep_rets.append(G)

        print(f"Episode {ep}: {G}")

    return policy, ep_rets


def update_policy(
    episode: List[Tuple[np.ndarray, int, float]],
    gamma: float,
    policy: Dict,
    Qvalue: Dict,
    Returns: Dict,
    env: TSP,
) -> float:
    G = 0
    for obs_, action, reward in reversed(episode):
        G = reward + gamma * G
        state_action_key = (env.loc, action)

        if state_action_key not in Returns:
            Returns[state_action_key] = []
        Returns[state_action_key].append(G)

        Qvalue[state_action_key] = np.mean(Returns[state_action_key])

        best_action = max(
            range(env.action_space.n),
            key=lambda a: Qvalue.get((env.loc, a), float('-inf')),
        )
        policy[env.loc] = best_action
    return G


def test_policy(env: TSP, policy: Dict) -> None:
    for i in range(env.num_targets):
        action = policy[env.loc]
        obs_, reward, terminated, truncated, info = env.step(action)
        print(f"Go to {action}")


if __name__ == "__main__":
    num_targets = 6
    max_episodes = 15000
    max_steps = 10
    gamma = 0.9

    env = TSP(num_targets)
    policy, ep_rets = train_tsp(env, max_episodes, max_steps, gamma)

    print(f"Average return: {np.mean(ep_rets)}")

    print("\nTesting policy:")
    test_policy(env, policy)
    print(policy)