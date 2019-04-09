from Agents.DQN_Agents.DQN_Agent import DQN_Agent
from Agents.HER_Base import HER_Base

class DQN_HER_Agent(DQN_Agent, HER_Base):
    """DQN algorithm with hindsight experience replay"""
    agent_name = "DQN-HER"

    def __init__(self, config):
        DQN_Agent.__init__(self, config)
        HER_Base.__init__(self, self.hyperparameters["buffer_size"], self.hyperparameters["batch_size"],
                          self.hyperparameters["HER_sample_proportion"])

    def step(self):
        """Runs a step within a game including a learning step if required"""
        while not self.done:
            self.pick_and_conduct_action()
            self.update_next_state_reward_done_and_score()
            if self.time_for_q_network_to_learn():
                self.q_network_learn(experiences=self.sample_from_HER_and_Ordinary_Buffer())
            self.track_episodes_data()
            self.save_experience()
            if self.done: self.save_alternative_experience()
            self.state = self.next_state  # this is to set the state for the next iteration
            self.global_step_number += 1
        self.episode_number += 1

    def enough_experiences_to_learn_from(self):
        return len(self.memory) > self.ordinary_buffer_batch_size and len(self.HER_memory) > self.HER_buffer_batch_size