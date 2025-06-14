import json
import os

# Globals for loaded data
QUESTIONS_DATA = {}
RUBRICS_DATA = {}
AXIS_MAPPING_DATA = {}

# Constants for ideological stance scores
MIN_STANCE_SCORE = -2
MAX_STANCE_SCORE = 2
STANCE_SCORE_LEVELS = list(range(MIN_STANCE_SCORE, MAX_STANCE_SCORE + 1)) # [-2, -1, 0, 1, 2]


def load_data_from_json(filepath, global_var_name):
    """Generic function to load JSON data from a file into a global variable."""
    global QUESTIONS_DATA, RUBRICS_DATA, AXIS_MAPPING_DATA

    data_container = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_json = json.load(f)
            if isinstance(loaded_json, list) and loaded_json and isinstance(loaded_json[0], dict) and 'id' in loaded_json[0]: # For questions.json
                 data_container = {item['id']: item for item in loaded_json}
            elif isinstance(loaded_json, list) and loaded_json and isinstance(loaded_json[0], dict) and 'rubric_id' in loaded_json[0]: # For rubrics.json
                data_container = {item['rubric_id']: item for item in loaded_json}
            elif isinstance(loaded_json, dict): # For axis_mapping.json or other dict-based JSON
                data_container = loaded_json
            else:
                print(f"Warning: Unrecognized or empty JSON structure in {filepath}")
                data_container = loaded_json

        if global_var_name == "QUESTIONS_DATA":
            QUESTIONS_DATA = data_container
        elif global_var_name == "RUBRICS_DATA":
            RUBRICS_DATA = data_container
        elif global_var_name == "AXIS_MAPPING_DATA":
            AXIS_MAPPING_DATA = data_container

        print(f"Successfully loaded {len(data_container)} items from {filepath} into {global_var_name}")
        return data_container
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
    except Exception as e:
        print(f"An unexpected error occurred while loading {filepath}: {e}")

    if global_var_name == "QUESTIONS_DATA":
        QUESTIONS_DATA = {}
    elif global_var_name == "RUBRICS_DATA":
        RUBRICS_DATA = {}
    elif global_var_name == "AXIS_MAPPING_DATA":
        AXIS_MAPPING_DATA = {}
    return None

def get_question_by_id(question_id):
    return QUESTIONS_DATA.get(question_id)

def get_rubric_by_id(rubric_id):
    return RUBRICS_DATA.get(rubric_id)

def prompt_for_manual_scores(question_obj, rubrics_data, axis_mapping_data):
    if not question_obj or 'scoring_rubric_ids' not in question_obj:
        print("Error: Invalid question object or no scoring rubrics defined.")
        return None

    manual_scores = {"question_id": question_obj['id']}
    print(f"\n--- Scoring Question ID: {question_obj['id']} ---")
    print(f"Question: {question_obj['question_text']}")

    for rubric_id in question_obj['scoring_rubric_ids']:
        rubric = rubrics_data.get(rubric_id)
        if not rubric:
            print(f"Warning: Rubric ID '{rubric_id}' not found. Skipping.")
            continue

        print(f"\n-- Rubric: {rubric['rubric_name']} --")
        print(f"   Description: {rubric['description']}")
        for level in rubric['levels']:
            print(f"   [{level['score']}] {level['description']}")

        while True:
            try:
                if not os.isatty(0):
                    score = -1
                    print(f"Non-interactive: Defaulting score for {rubric_id} to {score}.")
                else:
                    score_input = input(f"Enter score for {rubric['rubric_name']} (0-{len(rubric['levels'])-1}): ")
                    score = int(score_input)

                if score == -1 or (0 <= score < len(rubric['levels'])):
                    manual_scores[rubric_id] = score
                    break
                else:
                    print(f"Invalid score. Please enter a number between 0 and {len(rubric['levels'])-1}, or -1 for non-interactive default.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except EOFError:
                print(f"EOFError: No input. Defaulting score for {rubric_id} to -1.")
                manual_scores[rubric_id] = -1
                break

    q_axis_info = axis_mapping_data.get(question_obj['id'])
    if question_obj.get("module") == "A" and q_axis_info:
        if q_axis_info.get("type") == "choice":
            print(f"\n-- Ideological Choice for Axis: {q_axis_info['axis']} --")
            possible_choices = list(q_axis_info.get("scoring", {}).keys())
            possible_choices_str = f" ({', '.join(possible_choices)})" if possible_choices else " (e.g., a, b, c)"

            while True:
                try:
                    if not os.isatty(0):
                        choice_input = "N/A"
                        print(f"Non-interactive: Defaulting selected_choice to {choice_input}.")
                    else:
                        choice_input = input(f"Enter selected choice{possible_choices_str}: ").strip().lower()

                    if choice_input == "N/A" or \
                       (q_axis_info.get("scoring") and choice_input in q_axis_info["scoring"]) or \
                       (not q_axis_info.get("scoring") and choice_input):
                        manual_scores['selected_choice'] = choice_input
                        break
                    elif not choice_input and not q_axis_info.get("scoring"):
                         manual_scores['selected_choice'] = ""
                         break
                    else:
                        print(f"Invalid choice. Please enter one of {possible_choices_str} or N/A (or any if not predefined).")
                except EOFError:
                    print(f"EOFError: No input. Defaulting selected_choice to N/A.")
                    manual_scores['selected_choice'] = "N/A"
                    break

        elif q_axis_info.get("type") == "analytical_stance":
            print(f"\n-- Ideological Stance Score for Axis: {q_axis_info['axis']} --")
            print(f"   Score indicates direction: {MIN_STANCE_SCORE} (strong lean one way) to {MAX_STANCE_SCORE} (strong lean other way), 0 for neutral/balanced.")
            while True:
                try:
                    if not os.isatty(0):
                        stance_score = 0
                        print(f"Non-interactive: Defaulting ideological_stance_score to {stance_score}.")
                    else:
                        score_input = input(f"Enter ideological stance score ({MIN_STANCE_SCORE} to {MAX_STANCE_SCORE}): ")
                        stance_score = int(score_input)

                    if stance_score == 0 or (MIN_STANCE_SCORE <= stance_score <= MAX_STANCE_SCORE) :
                        manual_scores['ideological_stance_score'] = stance_score
                        break
                    else:
                        print(f"Invalid score. Please enter a number between {MIN_STANCE_SCORE} and {MAX_STANCE_SCORE}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                except EOFError:
                    print(f"EOFError: No input. Defaulting ideological_stance_score to 0.")
                    manual_scores['ideological_stance_score'] = 0
                    break

    print("--- End of Scoring for this Question ---")
    return manual_scores

def calculate_single_axis_score(axis_name, scored_responses, axis_mapping, questions_data):
    raw_score = 0
    current_max_positive_score = 0
    current_max_negative_score = 0

    for response in scored_responses:
        question_id = response.get("question_id")
        question_obj = questions_data.get(question_id)

        if not question_obj or question_obj.get("module") != "A":
            continue

        q_map_info = axis_mapping.get(question_id)
        if not q_map_info or q_map_info.get("axis") != axis_name:
            continue

        if q_map_info.get("type") == "choice" and q_map_info.get("scoring"):
            choice_scores = [s for s in q_map_info["scoring"].values() if isinstance(s, (int, float))]
            current_max_positive_score += max(0, max(choice_scores)) if choice_scores else 0
            current_max_negative_score += min(0, min(choice_scores)) if choice_scores else 0
        elif q_map_info.get("type") == "analytical_stance":
            current_max_positive_score += MAX_STANCE_SCORE
            current_max_negative_score += MIN_STANCE_SCORE

        clarity_score = response.get('position_clarity', 0)
        if clarity_score < 2:
            continue

        question_points = 0
        if q_map_info.get("type") == "choice":
            selected_choice = response.get("selected_choice")
            if selected_choice and q_map_info.get("scoring"):
                question_points = q_map_info["scoring"].get(selected_choice, 0)
        elif q_map_info.get("type") == "analytical_stance":
            question_points = response.get("ideological_stance_score", 0)

        raw_score += question_points

    effective_max_abs_score = max(current_max_positive_score, abs(current_max_negative_score))
    if effective_max_abs_score == 0:
        return 0.0

    normalized_score = (raw_score / effective_max_abs_score) * 10.0
    return round(max(-10.0, min(10.0, normalized_score)), 2)


def get_ideological_coordinates(all_scored_module_a_responses, axis_mapping, questions_data):
    coordinates = {}
    axes = ["Economic", "Social", "Authority", "Global"]
    for axis in axes:
        coordinates[f"{axis.lower()}_axis"] = calculate_single_axis_score(
            axis,
            all_scored_module_a_responses,
            axis_mapping,
            questions_data
        )
    return coordinates

if __name__ == '__main__':
    try:
        script_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(script_dir)
    except NameError:
        project_root = os.getcwd()

    questions_file = os.path.join(project_root, "data", "questions.json")
    rubrics_file = os.path.join(project_root, "data", "rubrics.json")
    axis_map_file = os.path.join(project_root, "data", "axis_mapping.json")

    if not os.path.exists(questions_file):
        questions_file = "data/questions.json"
    if not os.path.exists(rubrics_file):
        rubrics_file = "data/rubrics.json"
    if not os.path.exists(axis_map_file):
        axis_map_file = "data/axis_mapping.json"

    print(f"Attempting to load questions from: {os.path.abspath(questions_file)}")
    load_data_from_json(questions_file, "QUESTIONS_DATA")

    print(f"Attempting to load rubrics from: {os.path.abspath(rubrics_file)}")
    load_data_from_json(rubrics_file, "RUBRICS_DATA")

    print(f"Attempting to load axis mapping from: {os.path.abspath(axis_map_file)}")
    load_data_from_json(axis_map_file, "AXIS_MAPPING_DATA")

    if QUESTIONS_DATA and RUBRICS_DATA and AXIS_MAPPING_DATA:
        print("\n--- Starting Ideological Coordinate Calculation Test ---")

        mock_scored_module_a_responses = [
            {"question_id": "A1.GR.1", "position_clarity": 3, "selected_choice": "a"},
            {"question_id": "A1.GR.2", "position_clarity": 2, "ideological_stance_score": -1},
            {"question_id": "A1.GR.3", "position_clarity": 3, "selected_choice": "b"},
            {"question_id": "A1.GR.9", "position_clarity": 2, "ideological_stance_score": 1},
            {"question_id": "A2.MR.1", "position_clarity": 3, "selected_choice": "c"},
            {"question_id": "A2.MR.3", "position_clarity": 1, "ideological_stance_score": 1},
            {"question_id": "A3.GIE.1", "position_clarity": 3, "ideological_stance_score": -2},
            {"question_id": "A4.CET.1", "position_clarity": 3, "ideological_stance_score": 2},
            {"question_id": "A4.CET.3", "position_clarity": 3, "ideological_stance_score": 1},
            {"question_id": "A5.GIL.1", "position_clarity": 2, "ideological_stance_score": -1},
            {"question_id": "A5.GIL.4", "position_clarity": 3, "ideological_stance_score": -1},
        ]

        for resp in mock_scored_module_a_responses:
            question_data = QUESTIONS_DATA.get(resp["question_id"])
            if question_data:
                for rubric_id_def in question_data.get("scoring_rubric_ids", []):
                    if rubric_id_def not in resp:
                        resp[rubric_id_def] = 0

        coordinates = get_ideological_coordinates(mock_scored_module_a_responses, AXIS_MAPPING_DATA, QUESTIONS_DATA)
        print("\n--- Calculated Ideological Coordinates (Full Test) ---")
        print(json.dumps(coordinates, indent=2))
        print("--- Test Script Completed ---")
    else:
        print("\nCould not load all necessary data. Aborting test.")

```
