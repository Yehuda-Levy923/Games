import json
import os


class HighScoreManager:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        """Load high scores from file, create empty dict if file doesn't exist"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_scores(self):
        """Save current scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except IOError:
            print(f"Error saving high scores to {self.filename}")

    def get_high_score(self, game_name):
        """Get high score for a specific game"""
        return self.scores.get(game_name, 0)

    def update_high_score(self, game_name, score):
        """Update high score if new score is higher"""
        current_high = self.get_high_score(game_name)
        if score > current_high:
            self.scores[game_name] = score
            self.save_scores()
            return True  # New high score!
        return False  # Not a new high score

    def get_all_scores(self):
        """Get all high scores"""
        return self.scores.copy()

    def reset_score(self, game_name):
        """Reset high score for a specific game"""
        if game_name in self.scores:
            del self.scores[game_name]
            self.save_scores()

    def reset_all_scores(self):
        """Reset all high scores"""
        self.scores = {}
        self.save_scores()