// DTF.js

// DTF ve NIV Süreleri Verileri
const dtf_degerleri = [29.41, 25.00, 31.82, 19.05, 28.00, 37.50, 33.33, 7.14,
    128.57, 125.00, 58.82, 60.87, 53.33, 43.75, 87.50, 80.00,
    57.89, 43.75, 77.78, 66.67, 58.82, 75.00, 104.55, 91.67,
    92.31, 86.36, 90.48];
const niv_sureleri = [100, 52, 79, 50, 90, 92, 73, 73, 13, 9, 16, 7, 20, 13, 29, 27,
    21, 36, 2, 12, 29, 12, 10, 14, 33, 21, 10];

// Basit bir scaler fonksiyonu
function scaleData(data, mean, std) {
    return data.map(x => (x - mean) / std);
}

// Ortalama ve standart sapma hesaplama
function calculateMean(data) {
    return data.reduce((a, b) => a + b, 0) / data.length;
}

function calculateStd(data, mean) {
    const variance = data.reduce((sum, x) => sum + Math.pow(x - mean, 2), 0) / data.length;
    return Math.sqrt(variance);
}

// Veriyi ölçeklendirme
const dtf_mean = calculateMean(dtf_degerleri);
const dtf_std = calculateStd(dtf_degerleri, dtf_mean);
const niv_mean = calculateMean(niv_sureleri);
const niv_std = calculateStd(niv_sureleri, niv_mean);

const dtf_scaled = scaleData(dtf_degerleri, dtf_mean, dtf_std);
const niv_scaled = scaleData(niv_sureleri, niv_mean, niv_std);

// Basit bir SVR yerine Linear Regression (yaklaşım)
function linearRegression(x, y) {
    const n = x.length;
    const xMean = calculateMean(x);
    const yMean = calculateMean(y);

    let numerator = 0;
    let denominator = 0;
    
    for (let i = 0; i < n; i++) {
        numerator += (x[i] - xMean) * (y[i] - yMean);
        denominator += Math.pow((x[i] - xMean), 2);
    }

    const slope = numerator / denominator;
    const intercept = yMean - slope * xMean;

    return { slope, intercept };
}

const model = linearRegression(dtf_scaled, niv_scaled);

// DTF Değerine göre NIV Süresini Tahmin Et
function predictNIV(dtf_value) {
    const dtf_scaled = (dtf_value - dtf_mean) / dtf_std;
    const niv_scaled_pred = model.slope * dtf_scaled + model.intercept;
    const niv_pred = niv_scaled_pred * niv_std + niv_mean;
    return niv_pred;
}

// Tarayıcıdaki formdan alınan değerlerle hesaplama yap
document.getElementById('calculate-btn').addEventListener('click', function () {
    const inspiryum_kalinligi = parseFloat(document.getElementById('inspiryum').value);
    const ekspiryum_kalinligi = parseFloat(document.getElementById('ekspiryum').value);

    if (isNaN(inspiryum_kalinligi) || isNaN(ekspiryum_kalinligi)) {
        document.getElementById('result').innerHTML = 'Lütfen geçerli sayılar giriniz.';
        return;
    }

    if (ekspiryum_kalinligi === 0) {
        document.getElementById('result').innerHTML = 'Ekspiryum kalınlığı 0 olamaz.';
        return;
    }

    const dtf = ((inspiryum_kalinligi - ekspiryum_kalinligi) / ekspiryum_kalinligi) * 100;
    const nivTahmin = predictNIV(dtf);

    document.getElementById('result').innerHTML = `DKF (%): ${dtf.toFixed(2)}<br><br>Tahmini NIV süresi (saat): ${nivTahmin.toFixed(2)}`;
});
