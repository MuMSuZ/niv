from flask import Flask, request, render_template
from waitress import serve
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# DTF (%) ve NIV süreleri (saat)
dtf_degerleri = np.array([29.41, 25.00, 31.82, 19.05, 28.00, 37.50, 33.33, 7.14,
                          128.57, 125.00, 58.82, 60.87, 53.33, 43.75, 87.50, 80.00,
                          57.89, 43.75, 77.78, 66.67, 58.82, 75.00, 104.55, 91.67,
                          92.31, 86.36, 90.48])  
niv_sureleri = np.array([100, 52, 79, 50, 90, 92, 73, 73, 13, 9, 16, 7, 20, 13, 29, 27,
                         21, 36, 2, 12, 29, 12, 10, 14, 33, 21, 10])  

# Verileri ölçeklendirme
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(dtf_degerleri.reshape(-1, 1))
y_scaled = scaler_y.fit_transform(niv_sureleri.reshape(-1, 1))

# SVR modelini oluşturma ve eğitme
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
model.fit(X_scaled, y_scaled)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        inspiryum_kalinligi = float(request.form['inspiryum'])
        ekspiryum_kalinligi = float(request.form['ekspiryum'])
        if ekspiryum_kalinligi == 0:
            return render_template('index.html', result="Ekspiryum kalınlığı 0 olamaz.")
        dtf = ((inspiryum_kalinligi - ekspiryum_kalinligi) / ekspiryum_kalinligi) * 100
        dtf_scaled = scaler_X.transform(np.array([[dtf]]))
        niv_tahmin_scaled = model.predict(dtf_scaled)
        niv_tahmin = scaler_y.inverse_transform(niv_tahmin_scaled.reshape(-1, 1)).ravel()
        result = f"DKF (%): {dtf:.2f}\n\nTahmini NIV süresi (saat): {niv_tahmin[0]:.2f}"
        return render_template('index.html', result=result)
    except ValueError:
        return render_template('index.html', result="Lütfen geçerli sayılar giriniz.")

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)