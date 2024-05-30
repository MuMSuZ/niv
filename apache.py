def calculate_apache_ii(age, gcs, temp, map, hr, rr, pao2, ph, na, k, cr, hct, wbc, chronic_health):
    # Yaş için puan
    if age >= 75:
        age_score = 6
    elif age >= 65:
        age_score = 5
    elif age >= 55:
        age_score = 3
    elif age >= 45:
        age_score = 2
    else:
        age_score = 0

    # Kronik sağlık durumu için puan
    if chronic_health:
        chronic_score = 5
    else:
        chronic_score = 0

    # Diğer parametrelerin puanlarını hesaplamak için örnek bir yaklaşım
    # Bu örnek, gerçek APACHE II hesaplamasının tamamını temsil etmez ve sadece fikir vermek amaçlıdır.
    
    # GCS puanı (toplam 15 - GCS değeri)
    gcs_score = 15 - gcs
    
    # Vücut ısısı (örnek puanlama)
    if temp < 29 or temp > 40.9:
        temp_score = 4
    elif temp >= 39 or temp <= 30.9:
        temp_score = 3
    elif temp >= 38.5 or temp <= 31.9:
        temp_score = 1
    else:
        temp_score = 0

    # Ortalama Arteriyel Basınç (MAP)
    if map < 50:
        map_score = 4
    elif map >= 160:
        map_score = 4
    elif map >= 130 or map <= 70:
        map_score = 2
    else:
        map_score = 0

    # Diğer parametrelerin puanları da benzer şekilde hesaplanır
    # ...

    # Tüm puanların toplamı
    apache_ii_score = age_score + chronic_score + gcs_score + temp_score + map_score # + diğer puanlar
    
    return apache_ii_score

# Örnek kullanım
score = calculate_apache_ii(age=55, gcs=14, temp=36.5, map=85, hr=90, rr=16, pao2=95, ph=7.4, na=140, k=4.0, cr=1.0, hct=40, wbc=8.0, chronic_health=False)
print(f"APACHE II Skoru: {score}")
