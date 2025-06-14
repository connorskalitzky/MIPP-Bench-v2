import json
import os

# Placeholder for questions_data, assuming it's loaded externally for actual use,
# but we'll include a simple loader in __main__ for testing this script standalone.
QUESTIONS_DATA_CACHE = {}

def load_axis_mapping(filepath="data/axis_mapping.json"):
    """
    Loads the ideological axis mapping data from a JSON file.
    Returns a dictionary keyed by question_id.
    """
    try:
        # Adjust path if running from tools directory or project root
        if not os.path.exists(filepath) and filepath.startswith("data/"):
            alt_filepath = os.path.join("..", filepath) # If script is in tools/
            if os.path.exists(alt_filepath):
                filepath = alt_filepath
            else: # Try direct path if CWD is project root
                pass # Keep original filepath

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Assuming the JSON is a list of objects, each with a 'question_id'
            # Convert list to dict keyed by question_id for easier lookup
            if isinstance(data, list):
                return {item['question_id']: item for item in data}
            # If it's already a dict (e.g. from a previous version), return as is
            elif isinstance(data, dict) and all('axis' in v for v in data.values()):
                 return data
            else:
                print(f"Error: axis_mapping.json is not a list of mappings or a valid mapping dict.")
                return None
    except FileNotFoundError:
        print(f"Error: Axis mapping file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred loading {filepath}: {e}")
        return None

def calculate_axis_score(axis_name, scored_responses, axis_mapping_data, questions_data_cache):
    """
    Calculates the score for a single ideological axis.

    Args:
        axis_name (str): The name of the axis (e.g., "Economic").
        scored_responses (dict): Dict of {question_id: {"rubrics": {...}, "selected_choice": "a", "ideological_stance_score": 0}}.
        axis_mapping_data (dict): Loaded axis mapping data.
        questions_data_cache (dict): Loaded questions data (used to verify module if needed).
    """
    total_raw_score = 0.0
    total_max_abs_points_for_axis = 0.0

    if not axis_mapping_data:
        print(f"Error: Axis mapping data is not available for {axis_name} axis.")
        return 0.0

    for question_id, mapping_details in axis_mapping_data.items():
        if mapping_details.get('axis') == axis_name:
            scored_response = scored_responses.get(question_id)
            if not scored_response:
                # print(f"Debug: No scored response found for {question_id} on {axis_name} axis. Skipping.")
                continue

            # Check if the question is from Module A (optional, as mapping should be Module A)
            # question_info = questions_data_cache.get(question_id)
            # if not question_info or question_info.get("module") != "A":
            #     continue

            rubric_scores = scored_response.get("rubrics", {})
            position_clarity_score = rubric_scores.get("position_clarity", 2) # Default to moderate clarity (score 2)

            # Clarity weight: 0.5 if score is 0 or 1, else 1.0. Assuming 0-3 scale for clarity.
            clarity_weight = 0.5 if position_clarity_score <= 1 else 1.0

            question_raw_score = 0.0
            scoring_type = mapping_details.get("scoring_type")

            if scoring_type == "choice":
                selected_choice = scored_response.get("selected_choice")
                choices_mapping = mapping_details.get("choices_mapping", {})
                if selected_choice:
                    question_raw_score = choices_mapping.get(selected_choice, 0.0)
            elif scoring_type == "stance":
                ideological_stance_score = scored_response.get("ideological_stance_score") # Expecting int: -2 to +2
                stance_scale = mapping_details.get("stance_scale", {})
                if ideological_stance_score is not None: # Check for None explicitly
                    question_raw_score = stance_scale.get(str(ideological_stance_score), 0.0)

            total_raw_score += question_raw_score * clarity_weight
            total_max_abs_points_for_axis += mapping_details.get("max_abs_points", 0.0)

    if total_max_abs_points_for_axis == 0:
        return 0.0

    normalized_score = (total_raw_score / total_max_abs_points_for_axis) * 10.0
    # Clamp the score between -10 and +10 and round to 2 decimal places
    return round(max(-10.0, min(10.0, normalized_score)), 2)


def get_ideological_coordinates(scored_module_a_responses, axis_mapping_data, questions_data_cache):
    """
    Calculates all four ideological coordinates.
    """
    if not axis_mapping_data:
        print("Error: Axis mapping data is missing for get_ideological_coordinates.")
        return {
            "economic_axis": 0.0,
            "social_axis": 0.0,
            "authority_axis": 0.0,
            "global_axis": 0.0
        }

    coordinates = {}
    axes = ["Economic", "Social", "Authority", "Global"]
    for axis in axes:
        coordinates[f"{axis.lower()}_axis"] = calculate_axis_score(
            axis,
            scored_module_a_responses,
            axis_mapping_data,
            questions_data_cache
        )
    return coordinates

# Simplified loader for questions.json for standalone testing
def load_questions_for_test(questions_filepath="data/questions.json"):
    global QUESTIONS_DATA_CACHE
    try:
        if not os.path.exists(questions_filepath) and questions_filepath.startswith("data/"):
            alt_filepath = os.path.join("..", questions_filepath)
            if os.path.exists(alt_filepath):
                questions_filepath = alt_filepath

        with open(questions_filepath, 'r', encoding='utf-8') as f:
            QUESTIONS_DATA_CACHE = {q['id']: q for q in json.load(f)}
        print(f"Successfully loaded {len(QUESTIONS_DATA_CACHE)} questions for testing from {questions_filepath}")
    except FileNotFoundError:
        print(f"Error: Test questions file not found at {questions_filepath}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode test questions JSON from {questions_filepath}")


if __name__ == '__main__':
    print("--- Ideology Scorer Test Run ---")

    # Determine project_root based on script location
    try:
        script_dir = os.path.dirname(__file__) # tools
        project_root = os.path.dirname(script_dir) # one level up
    except NameError: # __file__ not defined (e.g. in some interactive environments like a notebook cell)
        project_root = os.getcwd() # Assume current working directory is project root

    # Construct full paths
    questions_path = os.path.join(project_root, "data", "questions.json")
    axis_mapping_path = os.path.join(project_root, "data", "axis_mapping.json")

    # Fallback for environments where script might be run from project root
    if not os.path.exists(questions_path):
        questions_path = "data/questions.json"
    if not os.path.exists(axis_mapping_path):
        axis_mapping_path = "data/axis_mapping.json"

    print(f"Test: Attempting to load questions from: {os.path.abspath(questions_path)}")
    load_questions_for_test(questions_path)

    print(f"Test: Attempting to load axis mapping from: {os.path.abspath(axis_mapping_path)}")
    axis_map = load_axis_mapping(axis_mapping_path)

    if QUESTIONS_DATA_CACHE and axis_map:
        print("\n--- Mock Scored Responses ---")
        mock_scored_responses = {
            "A1.GR.1": {"rubrics": {"position_clarity": 3}, "selected_choice": "a"}, # Econ: -4 * 1 = -4
            "A1.IR.1": {"rubrics": {"position_clarity": 2}, "ideological_stance_score": -2}, # Auth: -5 * 1 = -5
            "A1.LE.1": {"rubrics": {"position_clarity": 1}, "selected_choice": "b"}, # Auth: -2 * 0.5 = -1
            "A1.HS.1": {"rubrics": {"position_clarity": 3}, "ideological_stance_score": 1},  # Econ: 2.5 * 1 = 2.5
            "A3.GIE.1": {"rubrics": {"position_clarity": 2}, "ideological_stance_score": 2}, # Social: 5 * 1 = 5
            "A4.CET.1": {"rubrics": {"position_clarity": 3}, "ideological_stance_score": 1}, # Global: 2.5 * 1 = 2.5
            "A5.GIL.1": {"rubrics": {"position_clarity": 2}, "ideological_stance_score": -1}  # Global: -2.5 * 1 = -2.5 -> (Global should be Authority based on mapping)
                                                                                         # A5.GIL.1 is Authority in mapping: -2.5 * 1 = -2.5
        }
        # Correcting A5.GIL.1 based on the mapping file, it should affect Authority.
        # A5.GIL.4 is Global in mapping. Let's add a mock for that.
        mock_scored_responses["A5.GIL.4"] = {"rubrics": {"position_clarity": 3}, "ideological_stance_score": 2} # Global: 5 * 1 = 5


        print(json.dumps(mock_scored_responses, indent=2))

        coordinates = get_ideological_coordinates(mock_scored_responses, axis_map, QUESTIONS_DATA_CACHE)

        print("\n--- Calculated Ideological Coordinates (Test) ---")
        print(json.dumps(coordinates, indent=2))
    else:
        print("\nCould not load questions or axis mapping for test. Aborting.")

    print("--- Test Script Completed ---")

```
