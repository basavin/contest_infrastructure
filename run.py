# Put this script, submissions folder and skeleton-code folder in the same place
# E.g. you need the following directory structure:
# Grading-folder/
# --- submissions-folder/
# --- contest-folder/
# --- run.py
# --- match.py


import sys
import os
import subprocess
import operator
from multiprocessing import Pool
from match import Match

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
   
   print "Running games for" , first, "and", second, "..."
   output = subprocess.check_output([
            python_exec, "capture.py", 
            "-r", match.first_source,
            "-b", match.second_source,
            "--time", "10000",
            "--fixRandomSeed",
            "--layout", "layouts/defaultCapture.lay",
            "--numGames", str(3),
            "--super-quiet"
            ])

   found = False
   for line in output.split("\n"):
      if line.startswith("Scores:"):
         tokens = line.split(":")
         scores = tokens[1].strip().split(",")
         for score in scores:
            match.scores.append(int(score))
         found = True
         break
         
   if not found:
      print "Exception occurred when running!"
      match.error = True
   return match
   
 
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
            # no duplicates are ensured by calculating a hash-code
            matches.add(match)
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
            
            
def sort_teams_by_wins(matches):
   winners = dict()
   for match in matches:
      winner = match.winner
      if winner == "":
         continue
         
      if winner in winners:
         winners[winner] +=1
      else:
         winners[winner] = 1      
         
   sorted_tuples = sorted(winners.items(), key=operator.itemgetter(1), reverse=True)   
   return sorted_tuples

if __name__ == '__main__':
   # get the names of all students with complete submissions
   students = extract_student_names()
    
   print "Number of submissions:", len(students), "\n"
    
   # pair up the student teams
   matches = create_matches(students)
   print "Total matches to be played:", len(matches), "\n"
   # locate the source for their teams
   locate_source_files(matches)
   
   p = Pool(processes = 4)
   matches = p.map(run_match, matches)
 
   report = root_dir + "/" + "report.txt"
   if os.path.exists(report):
      os.remove(report)
   report_file = open(report, "w")
      
   report_file.write("Results of each 3-game series between two teams: \n \n")
   for match in matches:
      match.determine_winner()
      report_file.write(str(match) +"\n")
   print "\n"
            
   report_file.write("\nTeams sorted by the amount of 3-game series that they won: \n \n")
   sorted_tuples= sort_teams_by_wins(matches)
   for (winner, wins) in sorted_tuples:
      report_file.write(winner + " won " + str(wins) + " games " +"\n")
   report_file.close()
   print "Done."
   
   
      
   
      
   
   
