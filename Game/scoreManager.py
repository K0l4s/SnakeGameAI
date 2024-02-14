class ScoreManager:
  def __init__(self):
    self.scores = []
  
  def add_score(self, score):
    if score not in self.scores:
      self.scores.append(score)
      self.scores.sort(reverse=True)
      self.scores = self.scores[:10]

  def get_high_scores(self):
    return self.scores