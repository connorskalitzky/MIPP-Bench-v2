import json
import os # Added for potential path manipulations

# Placeholder for questions data
QUESTIONS_DATA = {}
# Placeholder for rubrics data
RUBRICS_DATA = {}

def load_questions(questions_filepath="data/questions.json"):
    """Loads questions from the specified JSON file."""
    global QUESTIONS_DATA
    try:
        with open(questions_filepath, 'r', encoding='utf-8') as f:
            QUESTIONS_DATA = {q['id']: q for q in json.load(f)}
        print(f"Successfully loaded {len(QUESTIONS_DATA)} questions from {questions_filepath}")
        return QUESTIONS_DATA
    except FileNotFoundError:
        print(f"Error: Questions file not found at {questions_filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {questions_filepath}")
        return None

def load_rubrics(rubrics_filepath="data/rubrics.json"):
    """Loads rubrics from the specified JSON file."""
    global RUBRICS_DATA
    try:
        with open(rubrics_filepath, 'r', encoding='utf-8') as f:
            RUBRICS_DATA = {r['rubric_id']: r for r in json.load(f)}
        print(f"Successfully loaded {len(RUBRICS_DATA)} rubrics from {rubrics_filepath}")
        return RUBRICS_DATA
    except FileNotFoundError:
        print(f"Error: Rubrics file not found at {rubrics_filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {rubrics_filepath}")
        return None

def get_question_by_id(question_id):
    """Retrieves a specific question by its ID."""
    return QUESTIONS_DATA.get(question_id)

def get_rubric_by_id(rubric_id):
    """Retrieves a specific rubric by its ID."""
    return RUBRICS_DATA.get(rubric_id)

def prompt_for_manual_scores(question_obj, rubrics_data):
    """
    Prompts a human evaluator to enter scores for a given question based on applicable rubrics.

    Args:
        question_obj (dict): The question object.
        rubrics_data (dict): A dictionary of all loaded rubrics.

    Returns:
        dict: A dictionary of manually entered scores, e.g., {"position_clarity": 2}
                Returns None if the question object is invalid or has no rubrics.
    """
    if not question_obj or 'scoring_rubric_ids' not in question_obj:
        print("Error: Invalid question object or no scoring rubrics defined for it.")
        return None

    manual_scores = {}
    print(f"\n--- Scoring Question ID: {question_obj['id']} ---")
    print(f"Question: {question_obj['question_text']}")

    for rubric_id in question_obj['scoring_rubric_ids']:
        rubric = rubrics_data.get(rubric_id)
        if not rubric:
            print(f"Warning: Rubric ID '{rubric_id}' not found in loaded rubrics. Skipping.")
            continue

        print(f"\n-- Rubric: {rubric['rubric_name']} --")
        print(f"   Description: {rubric['description']}")
        for level in rubric['levels']:
            print(f"   [{level['score']}] {level['description']}")

        while True:
            try:
                # Check for non-interactive environment for input()
                if not os.isatty(0):
                    print(f"Non-interactive environment: Defaulting score for {rubric_id} to -1.")
                    manual_scores[rubric_id] = -1 # Default score for non-interactive
                    break
                score_input = input(f"Enter score for {rubric['rubric_name']} (0-{len(rubric['levels'])-1}): ")
                score = int(score_input)
                if 0 <= score < len(rubric['levels']):
                    manual_scores[rubric_id] = score
                    break
                else:
                    print(f"Invalid score. Please enter a number between 0 and {len(rubric['levels'])-1}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except EOFError: # Specifically catch EOFError if input stream ends
                print(f"EOFError: No input available (non-interactive environment?). Defaulting score for {rubric_id} to -1.")
                manual_scores[rubric_id] = -1
                break

    print("--- End of Scoring for this Question ---")
    return manual_scores

def score_response(question_id, response_text="[Sample Response Text - Not Used in Manual Scoring Yet]"):
    """
    Orchestrates the scoring of a response to a given question.
    Currently focuses on prompting for manual scores.

    Args:
        question_id (str): The ID of the question being answered.
        response_text (str): The text of the model's response.

    Returns:
        dict: A dictionary of manual scores, or None if scoring fails.
    """
    if not QUESTIONS_DATA or not RUBRICS_DATA:
        print("Error: Questions or rubrics data not loaded globally. Please ensure they are loaded before calling score_response.")
        # In a real application, you might pass QUESTIONS_DATA and RUBRICS_DATA as arguments
        # or ensure they are initialized by a class that score_response is a method of.
        # For this script structure, we rely on them being populated by load_questions/load_rubrics
        # typically called from __main__ or a similar entry point.
        return None # Or handle by trying to load them, but path context is tricky here.

    question = get_question_by_id(question_id)
    if not question:
        print(f"Error: Question ID '{question_id}' not found in QUESTIONS_DATA.")
        return None

    print(f"Model Response to Q:{question_id}: '{response_text}'")

    manual_scores = prompt_for_manual_scores(question, RUBRICS_DATA)
    return manual_scores

# --- Update to the main execution for testing ---
# The following code should REPLACE the existing if __name__ == '__main__': block
# in tools/scorer.py to test the new scoring functionality.

if __name__ == '__main__':
    # import os # Already imported at the top

    script_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(script_dir)

    # Default paths, assuming 'data' is a sibling to 'tools' directory, or script is run from project root.
    # For the tool environment, files are at the root, so data/ will be at the root.
    questions_file = os.path.join(project_root, "data/questions.json")
    rubrics_file = os.path.join(project_root, "data/rubrics.json")

    print(f"Attempting to load questions from: {questions_file}")
    loaded_q = load_questions(questions_filepath=questions_file) # Populates global QUESTIONS_DATA

    print(f"Attempting to load rubrics from: {rubrics_file}")
    loaded_r = load_rubrics(rubrics_filepath=rubrics_file) # Populates global RUBRICS_DATA

    if loaded_q and loaded_r:
        print("\n--- Starting Test Scoring ---")
        # Test with a question that has rubrics defined
        # A3.GIE.1 is specified in the prompt
        test_question_id = "A3.GIE.1"

        if test_question_id not in QUESTIONS_DATA:
            print(f"Warning: Test question ID '{test_question_id}' does not exist in loaded questions.")
            if "A1.1.1" in QUESTIONS_DATA: # A common fallback used in previous examples
                test_question_id = "A1.1.1"
                print(f"Falling back to test question ID: {test_question_id}")
            elif QUESTIONS_DATA: # If any questions exist, use the first one
                test_question_id = list(QUESTIONS_DATA.keys())[0]
                print(f"Falling back to first available question ID: {test_question_id}")
            else:
                print("FATAL: No questions available to test. Exiting test.")
                test_question_id = None

        if test_question_id:
            print(f"Attempting to score question ID: {test_question_id}")
            # The subtask environment might not support input().
            # prompt_for_manual_scores is designed to default to -1 in such cases.
            scores = score_response(test_question_id, "This is a test response from the AI model.")

            if scores:
                print("\n--- Manual Scores Received ---")
                print(json.dumps(scores, indent=2))
            else:
                print(f"\nScoring process for Q_ID {test_question_id} did not return scores (it might have printed errors).")
    else:
        print("\nCould not load questions or rubrics. Aborting scoring test.")

```
