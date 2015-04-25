class Match:
   
   def __init__(self, first_team, second_team):
      
      self.first_team = first_team
      self.second_team = second_team
      self.key = tuple(sorted([self.first_team, self.second_team]))
      
      self.first_source = ""
      self.second_source = ""
      self.winner = ""
      self.error = False
      
      # this is a mapping {game -> score}
      # we assume three games, positive score indicates that the first team is a winner
      self.scores = list()
      
      
   # return true if one of the teams in the target team
   def has_team(self, team):
      return team in self.key

   def __str__(self):
      return "" + str(self.key) + " : " + str(self.scores)
   
   
      
   # implement the following two methods to be able to 
   # use Match objects as elements of set
   def __hash__(self):
      return hash(self.key)
   
   def __eq__(self, other):
      return self.key == other.key
   