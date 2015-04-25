import sys
import os
import subprocess
from match import Match
import operator


# PREREQUISITES: put this script, submissions folder and skeleton folder in the same place
# e.g. you need the following directory structure:
# Grading-folder
# --- submissions-folder
# --- contest-folder
# --- run.py

root_dir = os.getcwd()                          # directory where this script resides
contest_dir = root_dir + "/contest"             # contest project code
submissions_dir = root_dir + "/submissions"     # students' submitted files
#python_exec = '/s/python-2.7.3/bin/python2.7'  # path to python ver 2.7 exec
python_exec = sys.executable                    # use the same executable by default
 
 
def run_match(match):
   # make sure we are in the right folder
   os.chdir(contest_dir) 
   
   first = match.first_team
   second = match.second_team
    
   seeds = ['cs540', 'dima', 'madison']
   for i in range(3):
      print "---------------------------"
      print "Running a match #", str(i+1),  "for", first, "and", second, "..."
      
      exitCode = subprocess.call([
                                 python_exec, "capture.py", 
                                 "-r", match.first_source,
                                 "-b", match.second_source,
                                 "--time", "10000",
                                 "--fixRandomSeed", seeds[i],
                                 "--layout", "layouts/defaultCapture.lay",
                                 "--super-quiet"
                                 ])
      
      
      if exitCode != 0:
         print "Exception occurred when running!"
         match.error = True
         return
      else :
         # record the score
         score_file = open("score", "r")
         score = int(score_file.readline())
         match.scores.append(score)
   print "Done."
   print "---------------------------\n"
   

"""
   Remove compiled python files and score files from the contest 
   code folder to get ready for a new play
"""   
def clean_contest_code():
   # make sure we are in the right folder
   os.chdir(contest_dir) 
    
   
   for filename in os.listdir("."):
      # remove all compiled python files
      if filename.endswith(".pyc"):
         os.remove(filename)
      
      # remove "score" file:
      if filename == "score":
         os.remove(filename)
         
      # remove "replay-0" file:
      if filename == "replay-0":
         os.remove(filename)
   
   return True

"""
   Go through the folder with all students' submissions 
   and record all students' names
   
   Assume that each student submitted only one file
   of the following format: studentname_blah_blah.py
"""
def extract_student_names():
   # make sure we are in the right folder
   os.chdir(submissions_dir)
   
   # First remove all compiled .pyc files
   for filename in os.listdir("."):
      if filename.endswith(".pyc"):
         os.remove(filename)
    
   submissions = set()
   for filename in os.listdir("."):
      if filename.endswith(".py"):
         student = filename.split("_")[0]
         submissions.add(student)

   return sorted(submissions)


"""
   This function takes a set of teams and returns all pair of
   students that will later play against each other
   
   e.g. if we have student1, student2 and student3, the pairs will be 
   (student1, student2), (student1, student3) and (student2, student3)
"""
def create_matches(students):
   matches = set()
   for first in students:
      for second in students:
         if first != second:
            match = Match(first, second)
            matches.add(match)
            
#    for match in matches:
#       print match.first_team, match.second_team
   
   return matches


def locate_source_files(matches):
   # make sure we are in the right folder
   os.chdir(submissions_dir)
   
   for match in matches:
      
      for filename in os.listdir("."):
         
         full_path = submissions_dir + "/" + filename
         if filename.startswith(match.first_team):
            match.first_source = full_path
            
         if filename.startswith(match.second_team):
            match.second_source = full_path
            
def determine_winner(match):
   first_team_won = 0
   second_team_won = 0
   for score in match.scores:
      if score > 0:
         first_team_won += 1
      else:
         second_team_won +=1
         
   if first_team_won > second_team_won:
      match.winner = match.first_team
   elif first_team_won < second_team_won:
      match.winner = match.second_team
   else:
      match.winner = 'Tie!!'
            

if __name__ == '__main__':
   # get the names of all students with complete submissions
   students = extract_student_names()
   
   #print "Number of submissions:", len(students), "\n"
   
   # pair up the student teams
   matches = create_matches(students)
   print "Total matches to be played:", len(matches)
   # locate the source for their teams
   locate_source_files(matches)
   
   # run the matches
   i = 0;
   for match in matches:
      
      clean_contest_code()
      run_match(match)
      
      if match.error:
         print "Error occurred when running a match" + str(match)
         
      print match
      determine_winner(match)
      print "The winner is", match.winner
      i +=1 
      if i == 3 : break
   
   # determine the overall winner
   winners = dict()
   for match in matches:
      winner = match.winner
      if winner == "":
         continue
      
      if winner in winners:
         winners[winner] +=1
      else:
         winners[winner] = 1
         
   report = root_dir + "/" + "report.txt"
   if os.path.exists(report):
      os.remove(report)
   report_file = open(report, "w")
   
   report_file.write("Results of each 3-game series between two teams: \n \n")
   for match in matches:
      report_file.write(str(match) +"\n")
   print "\n"
         
   report_file.write("\n Teams sorted by the amount of 3-game series that they won: \n \n")
   sorted_x = sorted(winners.items(), key=operator.itemgetter(1), reverse=True)
   for (winner, wins) in sorted_x:
      report_file.write(winner + " won " + str(wins) + " games " +"\n")
   report_file.close()
      
   
   
