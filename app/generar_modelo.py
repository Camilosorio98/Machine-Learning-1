import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os

# 1. Crear carpeta output si no existe
os.makedirs('output', exist_ok=True)

# 2. Generar dataset balanceado
np.random.seed(42)
n_samples = 1000

study_hours = np.random.normal(20, 8, n_samples)
attendance = np.random.normal(85, 10, n_samples)
gpa = np.random.normal(3.5, 0.8, n_samples)

logit = 0.05*study_hours + 0.03*attendance + 0.4*gpa - 25
prob = 1 / (1 + np.exp(-logit))

pass_fail = []
for i in range(n_samples):
    if len(pass_fail) < 500:
        target_class = i % 2
    else:
        target_class = 1 - (len(pass_fail) % 2)
    pass_fail.append(target_class)

pass_fail = np.array(pass_fail)

df = pd.DataFrame({
    'study_hours': study_hours,
    'attendance': attendance,
    'gpa': gpa,
    'pass_fail': pass_fail
})

# Guardar CSV
df.to_csv('output/student_pass_fail.csv', index=False)
print("✅ student_pass_fail.csv guardado en output/")

# 3. Entrenar el modelo y escalar los datos
X = df[['study_hours', 'attendance', 'gpa']]
y = df['pass_fail']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# 4. Guardar el modelo y el scaler
with open('output/model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ model.pkl guardado en output/")

with open('output/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✅ scaler.pkl guardado en output/")
print("\n¡Todo listo! Ya puedes correr app.py")
