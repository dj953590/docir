retrieve data from the database using SQLAlchemy and calculate the F1-score as described, we need to connect to the database, query the y14_Run table, and process the data. Below is the updated Python program that uses SQLAlchemy for database interaction.
from sqlalchemy import create_engine, MetaData, Table, select
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# Database connection details
DATABASE_URI = 'your_database_uri_here'  # Replace with your actual database URI

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Define the metadata and table
metadata = MetaData()
y14_run_table = Table('y14_Run', metadata, autoload_with=engine)

# Query to retrieve data from the y14_Run table
query = select([
    y14_run_table.c.facility_id,
    y14_run_table.c.attribute_name,
    y14_run_table.c.confidence_level,
    y14_run_table.c.is_correct
])

# Execute the query and load the data into a DataFrame
with engine.connect() as connection:
    df = pd.read_sql(query, connection)

# Filter out entries with confidence level below 70%
df = df[df['confidence_level'] >= 70]

# Group by facility_id and attribute_name, and keep the row with the highest confidence level
df = df.sort_values('confidence_level', ascending=False).groupby(['facility_id', 'attribute_name']).first().reset_index()

# Initialize dictionaries to store true positives, false positives, and false negatives for each attribute
attributes = df['attribute_name'].unique()
true_positives = {attr: 0 for attr in attributes}
false_positives = {attr: 0 for attr in attributes}
false_negatives = {attr: 0 for attr in attributes}

# Calculate true positives, false positives, and false negatives for each attribute
for _, row in df.iterrows():
    attr = row['attribute_name']
    if row['is_correct']:
        true_positives[attr] += 1
    else:
        false_positives[attr] += 1

# Calculate false negatives by comparing with the total number of facilities
total_facilities = df['facility_id'].nunique()
for attr in attributes:
    false_negatives[attr] = total_facilities - true_positives[attr]

# Calculate precision, recall, and F1-score for each attribute
f1_scores = {}
for attr in attributes:
    precision = true_positives[attr] / (true_positives[attr] + false_positives[attr]) if (true_positives[attr] + false_positives[attr]) > 0 else 0
    recall = true_positives[attr] / (true_positives[attr] + false_negatives[attr]) if (true_positives[attr] + false_negatives[attr]) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    f1_scores[attr] = f1

# Calculate overall F1-score
overall_true_positives = sum(true_positives.values())
overall_false_positives = sum(false_positives.values())
overall_false_negatives = sum(false_negatives.values())

overall_precision = overall_true_positives / (overall_true_positives + overall_false_positives) if (overall_true_positives + overall_false_positives) > 0 else 0
overall_recall = overall_true_positives / (overall_true_positives + overall_false_negatives) if (overall_true_positives + overall_false_negatives) > 0 else 0
overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

# Print F1-scores for each attribute and the overall F1-score
for attr, f1 in f1_scores.items():
    print(f"F1-score for {attr}: {f1:.2f}")

print(f"Overall F1-score: {overall_f1:.2f}")

Explanation of Changes:
SQLAlchemy Setup:

The create_engine function is used to create a connection to the database using the provided DATABASE_URI.

The MetaData and Table objects are used to reflect the y14_Run table structure from the database.

Query Execution:

A select query is constructed to retrieve the required columns (facility_id, attribute_name, confidence_level, and is_correct) from the y14_Run table.

The query is executed using pd.read_sql, and the results are loaded into a Pandas DataFrame.

Data Processing:

The program filters out rows with a confidence level below 70%.

It groups the data by facility_id and attribute_name, keeping only the row with the highest confidence level for each group.

F1-score Calculation:

The program calculates true positives, false positives, and false negatives for each attribute.

It computes the precision, recall, and F1-score for each attribute and the overall F1-score for all attributes combined.

Output:

The program prints the F1-score for each attribute and the overall F1-score.

Notes:
Replace 'your_database_uri_here' with the actual connection string for your database (e.g., postgresql://user:password@localhost:5432/dbname).

Ensure that the y14_Run table exists in the database and contains the required columns (facility_id, attribute_name, confidence_level, and is_correct).

If the is_correct column is not available, you will need to add logic to determine the correctness of the extracted information.

This program provides a complete solution for retrieving data from the database using SQLAlchemy and calculating the F1-score for your RAG application.

what is F1 Score and what does it tells about the each of the attributes
What is F1 Score?
The F1 Score is a metric used to evaluate the performance of a classification model. It is the harmonic mean of two other metrics: Precision and Recall. The F1 Score ranges from 0 to 1, where:

1 indicates perfect precision and recall (ideal performance).

0 indicates poor performance (either precision or recall is 0).

The formula for F1 Score is:

F1 Score
=
2
×
Precision
×
Recall
Precision

Where:

Precision measures the accuracy of the positive predictions (how many of the predicted positives are actually correct).

Precision
=
True Positives (TP)
True Positives (TP)
+
False Positives (FP)
Precision= 
True Positives (TP)+False Positives (FP)
True Positives (TP)
​
 
Recall measures the ability of the model to identify all relevant instances (how many of the actual positives are correctly predicted).

Recall
=
True Positives (TP)
True Positives (TP)
+
False Negatives (FN)
Recall= 
True Positives (TP)+False Negatives (FN)
True Positives (TP)
​
What Does F1 Score Tell About Each Attribute?
In the context of your RAG application, the F1 Score is calculated for each of the 13 key attributes extracted from credit agreements and credit memos. Here's what the F1 Score tells you about each attribute:

Performance of Attribute Extraction:

The F1 Score indicates how well the model is extracting a specific attribute from the documents.

A high F1 Score (close to 1) means the model is both accurate (high precision) and thorough (high recall) in extracting that attribute.

A low F1 Score (close to 0) means the model is either missing many correct instances (low recall) or making many incorrect predictions (low precision).

Trade-off Between Precision and Recall:

If the F1 Score is low, you can investigate whether the issue is due to:

Low Precision: The model is extracting incorrect information for the attribute (too many false positives).

Low Recall: The model is failing to extract the attribute in many cases (too many false negatives).

Attribute-Specific Insights:

By calculating the F1 Score for each attribute, you can identify which attributes are being extracted well and which ones need improvement.

For example:

If attribute1 has an F1 Score of 0.9, it means the model is performing very well for this attribute.

If attribute2 has an F1 Score of 0.4, it means the model is struggling with this attribute, and you may need to improve the extraction logic or training data for it.

Overall Model Performance:

The overall F1 Score (calculated across all 13 attributes) gives you a single metric to evaluate the performance of the entire RAG application.

A high overall F1 Score indicates that the model is performing well across all attributes, while a low overall F1 Score suggests that the model needs improvement.

Example Interpretation
Suppose you calculate the F1 Score for the following attributes:

Attribute	F1 Score
attr1	0.95
attr2	0.80
attr3	0.60
attr4	0.40
attr1: The F1 Score of 0.95 indicates excellent performance. The model is both accurate and thorough in extracting this attribute.

attr2: The F1 Score of 0.80 indicates good performance, but there is some room for improvement (e.g., reducing false positives or false negatives).

attr3: The F1 Score of 0.60 suggests moderate performance. The model may be missing many correct instances (low recall) or making incorrect predictions (low precision).

attr4: The F1 Score of 0.40 indicates poor performance. The model is struggling with this attribute, and significant improvements are needed.

Why Use F1 Score Instead of Just Precision or Recall?
The F1 Score is particularly useful when:

Class Imbalance: There is an imbalance between the number of positive and negative instances (e.g., some attributes may appear rarely in the documents).

Trade-off Between Precision and Recall: You want to balance the importance of avoiding false positives (precision) and false negatives (recall).

For example:

If you only optimize for precision, the model might become too conservative and miss many correct instances (low recall).

If you only optimize for recall, the model might extract too many incorrect instances (low precision).

The F1 Score provides a single metric that balances both concerns, making it a robust measure of model performance.

Conclusion
The F1 Score is a critical metric for evaluating the performance of your RAG application in extracting the 13 key attributes. By calculating the F1 Score for each attribute, you can:

Identify which attributes are being extracted well and which ones need improvement.

Understand whether the model is struggling with precision, recall, or both.

Make data-driven decisions to improve the extraction logic, training data, or confidence thresholds.

The overall F1 Score provides a summary of the model's performance across all attributes, helping you assess the effectiveness of the entire system.

how is the false negative calculate in the program
In the provided program, false negatives (FN) are calculated based on the assumption that for each attribute, the total number of possible correct extractions is equal to the total number of unique facilities (total_facilities). Here's a detailed explanation of how false negatives are calculated:

Key Concepts
True Positives (TP):

The number of times the model correctly extracted the attribute for a facility.

False Positives (FP):

The number of times the model incorrectly extracted the attribute for a facility.

False Negatives (FN):

The number of times the model failed to extract the attribute for a facility when it should have.

Total Facilities:

The total number of unique facilities in the dataset. This represents the maximum number of times the attribute could have been correctly extracted.

How False Negatives Are Calculated
The formula used to calculate false negatives for each attribute is:

False Negatives (FN)
=
Total Facilities
−
True Positives (TP)
False Negatives (FN)=Total Facilities−True Positives (TP)
Explanation:
If the model correctly extracted the attribute for a facility, it is counted as a True Positive (TP).

If the model did not extract the attribute for a facility (or extracted it incorrectly), it is counted as a False Negative (FN).

Since the total number of facilities represents all possible opportunities to extract the attribute, the difference between the total facilities and the true positives gives the number of missed extractions (false negatives).

Example
Suppose:

There are 5 unique facilities in the dataset.

For a specific attribute (attr1), the model correctly extracted the attribute for 3 facilities (True Positives = 3).

Then:

False Negatives (FN)
=
Total Facilities
−
True Positives (TP)
=
5
−
3
=
2
False Negatives (FN)=Total Facilities−True Positives (TP)=5−3=2
This means the model failed to extract attr1 for 2 facilities.

Why This Approach Works
Assumption:

The program assumes that every facility should have the attribute extracted. If the model fails to extract the attribute for a facility, it is counted as a false negative.

Handling Multiple LLM Runs:

If there are multiple LLM runs for the same facility and attribute, the program keeps only the result with the highest confidence level (after filtering out results with confidence < 70%). This ensures that each facility is counted only once for each attribute.

Implicit Ground Truth:

The program uses the is_correct column to determine whether an extraction is correct (True Positive) or incorrect (False Positive). If the extraction is missing for a facility, it is implicitly treated as a False Negative.

Limitations
Missing Ground Truth:

If the is_correct column is not available, the program cannot calculate true positives or false positives. In such cases, you would need to manually label the data or use another method to determine correctness.

Assumption of Completeness:

The program assumes that every facility should have the attribute extracted. If some facilities do not have the attribute at all (e.g., the attribute is optional), this approach may overestimate false negatives.

Confidence Threshold:

The program filters out extractions with a confidence level below 70%. If the threshold is too high, it may increase false negatives; if it is too low, it may increase false positives.

Code Snippet for False Negative Calculation
Here’s the relevant part of the code that calculates false negatives:

python
Copy
# Calculate false negatives by comparing with the total number of facilities
total_facilities = df['facility_id'].nunique()
for attr in attributes:
    false_negatives[attr] = total_facilities - true_positives[attr]
Steps:
total_facilities = df['facility_id'].nunique():

Counts the total number of unique facilities in the dataset.

false_negatives[attr] = total_facilities - true_positives[attr]:

For each attribute, calculates the number of false negatives by subtracting the number of true positives from the total number of facilities.

Example Walkthrough
Input Data:
facility_id	attribute_name	confidence_level	is_correct
1	attr1	80	True
1	attr2	65	False
1	attr3	90	True
2	attr1	75	True
2	attr2	85	True
2	attr3	70	False
3	attr1	60	False
3	attr2	55	False
3	attr3	95	True
Steps:
Filter confidence ≥ 70%:

Rows with confidence_level < 70 are removed.

Group by facility and attribute, keep highest confidence:

For each facility and attribute, only the row with the highest confidence is kept.

Calculate True Positives (TP):

For attr1: TP = 2 (facility 1 and 2).

For attr2: TP = 1 (facility 2).

For attr3: TP = 2 (facility 1 and 3).

Calculate False Negatives (FN):

Total facilities = 3.

For attr1: FN = 3 - 2 = 1.

For attr2: FN = 3 - 1 = 2.

For attr3: FN = 3 - 2 = 1.

Conclusion
The false negatives are calculated as the difference between the total number of facilities and the number of true positives for each attribute. This approach provides a simple and effective way to measure how often the model fails to extract an attribute when it should have. However, it relies on the assumption that every facility should have the attribute extracted, which may need to be adjusted based on the specific requirements of your application.

New chat



