import sys
import os
import subprocess
from match import Match
import operator
from multiprocessing import Pool


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
   
   print "---------------------------"
   print "Running games for" , first, "and", second, "...",

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
   
   print "Done."
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
   print "---------------------------\n"
   
 
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
            

if __name__ == '__main__':
   # get the names of all students with complete submissions
   students = extract_student_names()
    
   print "Number of submissions:", len(students), "\n"
    
   # pair up the student teams
   matches = create_matches(students)
   print "Total matches to be played:", len(matches)
   # locate the source for their teams
   locate_source_files(matches)
   
   i = 0
   # run the matches
   for match in matches:
      run_match(match)
      match.determine_winner()
      print match
      print "The winner is", match.winner
      i +=1
      if i ==3:break
      

#    p = Pool(processes = 4)
#    test = [list(matches)[0], list(matches)[1], list(matches)[2]]
#    p.map(run_match, test)
   
#    print "WHAAAAAAA"
    
   #determine the overall winner
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
           
   report_file.write("\nTeams sorted by the amount of 3-game series that they won: \n \n")
   sorted_x = sorted(winners.items(), key=operator.itemgetter(1), reverse=True)
   for (winner, wins) in sorted_x:
      report_file.write(winner + " won " + str(wins) + " games " +"\n")
   report_file.close()
   
   
      
   
      
   
   
