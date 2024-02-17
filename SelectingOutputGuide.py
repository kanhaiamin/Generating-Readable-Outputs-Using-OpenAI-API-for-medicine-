import pandas as pd

# Load your data and insert your file names. Note, columns are in the format of P1-P36 for our case
#Using actual outputs
peds_outputs_all = pd.read_csv('Outputs36.csv')
#Only the average reading grade levels
peds_tool_aRGLS = pd.read_csv('argls36.csv')
#Word counts
peds_tool_word_counts = pd.read_csv('wordcounts36.csv')


def get_desired_column(condition, lower_bound, upper_bound, target_value):
    # Filter the grade levels for the given condition
    grade_levels = peds_tool_aRGLS[peds_tool_aRGLS["Condition"] == condition].iloc[0, 1:].astype(float)
    
    # Get the columns with grade levels between the bounds
    desired_columns = grade_levels[(grade_levels >= lower_bound) & (grade_levels <= upper_bound)]
    
    if not desired_columns.empty:
        # If there are multiple columns, select based on word count
        if len(desired_columns) > 1:
            word_counts = peds_tool_word_counts[peds_tool_word_counts["Condition"] == condition][desired_columns.index]
            return word_counts.idxmax(axis=1).values[0]
        else:
            return desired_columns.index[0]
    else:
        # If no columns in the desired range, select the column closest to the target value
        return (grade_levels - target_value).abs().idxmin()


def generate_csv(lower_bound, upper_bound, target_value, output_filename):
    conditions = peds_outputs_all["Condition"]
    selected_columns = conditions.apply(lambda x: get_desired_column(x, lower_bound, upper_bound, target_value))
    
    # Replacing the deprecated lookup method
    selected_texts = [peds_outputs_all[peds_outputs_all["Condition"] == cond][col].values[0] for cond, col in zip(conditions, selected_columns)]
    
    result_df = pd.DataFrame({"Condition": conditions, "SelectedText": selected_texts, "Prompt": selected_columns})
    result_df.to_csv(output_filename, index=False)


# Generate CSV files based on the four criteria; 
#Numbers are lower bound, upper bound, target value, and output file name
generate_csv(5.25, 5.75, 5.5, 'selected_texts_v1.csv')
generate_csv(7.25, 7.75, 7.5, 'selected_texts_v2.csv')
generate_csv(9.25, 9.75, 9.5, 'selected_texts_v3.csv')
generate_csv(11.25, 11.75, 11.5, 'selected_texts_v4.csv')

print("CSV files generated successfully!")
