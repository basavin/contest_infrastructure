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
      return "" + str(self.key) + " : " + str(self.scores) + " and the winner is " + self.winner
   
   
   def determine_winner(self):
      if self.error:
         self.winner = 'Error occurred'
         return
         
      first_team_won = 0
      second_team_won = 0
      
      for score in self.scores:
         if score > 0:
            first_team_won += 1
         elif score < 0 :
            second_team_won +=1
              
      if first_team_won > second_team_won:
         self.winner = self.first_team
      elif first_team_won < second_team_won:
         self.winner = self.second_team
      else:
         self.winner = 'Tie!!'

   # implement the following two methods to be able to 
   # use Match objects as elements of set
   def __hash__(self):
      return hash(self.key)
   
   def __eq__(self, other):
      return self.key == other.key
   