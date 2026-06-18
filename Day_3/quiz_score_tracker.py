# Quiz Game Score Tracker
#
# This program simulates a quiz game where players earn
# points for correct answers. Consecutive correct answers
# create a streak and can earn bonus points.
#
# The program demonstrates:
# - Global variables (total score, high score)
# - Nonlocal variables (session score, streak)
# - Nested functions
# - Closures (private counter for each player)
# - Python LEGB scope rule
#
# Session statistics and overall game statistics are
# displayed after the game.
 
 
 
 
# Global variables
total_score = 0
high_score = 0
BONUS_MULTIPLIER = 2
 
 
def game_session(player_name: str):
 
    # Enclosing Scope Variables
    session_score = 0
    streak = 0
 
    def answer_question(correct: bool, points: int):
 
        # Access enclosing variables
        nonlocal session_score, streak
 
        # Access global variables
        global total_score, high_score
 
        # Local variable
        earned_points = 0
 
        if correct:
            streak += 1
 
            earned_points = points
 
            if streak >= 2:
                earned_points *= BONUS_MULTIPLIER
                print(
                    f"{player_name} answered correctly! "
                    f"+{earned_points} (streak: {streak}) BONUS x{BONUS_MULTIPLIER}"
                )
            else:
                print(
                    f"{player_name} answered correctly! "
                    f"+{earned_points} (streak: {streak})"
                )
 
            session_score += earned_points
            total_score += earned_points
 
            if session_score > high_score:
                high_score = session_score
 
        else:
            print(
                f"{player_name} answered wrong. "
                f"Streak reset. (was {streak})"
            )
            streak = 0
 
    def get_session_stats():
 
        print(f"\n--- Session Stats for {player_name} ---")
        print("Session score :", session_score)
        print("Current streak:", streak)
        print("Global total  :", total_score)
        print("High score    :", high_score)
 
        # Built-in scope
        print("Questions answered:", abs(streak))
        print("Type of score:", type(session_score).__name__)
 
    return answer_question, get_session_stats
 
 
# Closure
def make_player_counter(player: str):
 
    count = 0
 
    def increment():
        nonlocal count
        count += 1
        print(f"{player} has played {count} game(s)")
        return count
 
    return increment
 
answer, stats = game_session("Chaitali")
 
answer(correct=True, points=10)
answer(correct=True, points=10)
answer(correct=True, points=10)
answer(correct=False, points=0)
answer(correct=True, points=10)
 
stats()
 
print("\n----------------------------")
 
rahul_counter = make_player_counter("Rahul")
 
rahul_counter()
rahul_counter()
rahul_counter()
 
