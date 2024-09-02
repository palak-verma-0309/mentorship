from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Mentorship Matching System!"

@app.route('/<student_name>', methods=['GET'])
def get_recommendations(student_name):
    students_df = pd.read_csv('students_dataset.csv')
    mentors_df = pd.read_csv('mentors_dataset.csv')

    students_df.fillna('', inplace=True)
    mentors_df.fillna('', inplace=True)

    students_df['Name'] = students_df['Name'].str.lower()
    mentors_df['Name'] = mentors_df['Name'].str.lower()

    student_categorical_columns = ['Gender', 'Future Career']
    mentor_categorical_columns = ['Gender', 'Skills', 'Current Position', 'Preferred Domain']

    for column in student_categorical_columns:
        le = LabelEncoder()
        students_df[column] = le.fit_transform(students_df[column])

    for column in mentor_categorical_columns:
        le = LabelEncoder()
        mentors_df[column] = le.fit_transform(mentors_df[column])

    common_features = ['GPA', 'Age'] + student_categorical_columns

    for feature in common_features:
        if feature not in mentors_df.columns:
            mentors_df[feature] = 0

    student_features = students_df[common_features]
    mentor_features = mentors_df[common_features]

    B = nx.Graph()
    students = students_df['Name'].tolist()
    mentors = mentors_df['Name'].tolist()

    B.add_nodes_from(students, bipartite=0)
    B.add_nodes_from(mentors, bipartite=1)

    combined_features = np.vstack((student_features, mentor_features))
    similarity_matrix = cosine_similarity(combined_features)

    num_students = len(students)
    for i in range(num_students):
        for j in range(num_students, len(combined_features)):
            B.add_edge(students[i], mentors[j - num_students], weight=similarity_matrix[i, j])

    def get_recommendations_for_student(student_name):
        student_name = student_name.lower()
        if student_name not in B:
            return f"Student '{student_name}' not found."
        recommendations = sorted(B[student_name], key=lambda x: B[student_name][x]['weight'], reverse=True)
        return recommendations

    recommendations = get_recommendations_for_student(student_name)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
