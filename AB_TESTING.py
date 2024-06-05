#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################
#C:\Users\User\PycharmProjects\pythonProject1\pythonProject\case study\ABTesti-case study\ab_testing.xlsx
######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.2f' % x)



# 1. Hipotezleri Kur
# - HO = M1 = M2 ==> Max. Bidding ile Ave. Bidding Arasında Anlamlı bir farkl. yoktur
# - H1 = M1 != M2 ==> vardır.
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df_sheet1 = pd.read_excel(r"C:\Users\User\PycharmProjects\pythonProject1\pythonProject\case study\ABTesti-case study\ab_testing.xlsx", sheet_name="Control Group")
df_sheet2 = pd.read_excel(r"C:\Users\User\PycharmProjects\pythonProject1\pythonProject\case study\ABTesti-case study\ab_testing.xlsx", sheet_name="Test Group")
df1 = df_sheet1.copy()
df2 = df_sheet2.copy()
# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df1)
check_df(df2)
# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df1["Bidding"] = "Maximum_Bidding"

df1.groupby("Bidding").agg({"Purchase": "mean"})

df2["Bidding"] = "Average_Bidding"

df2.groupby("Bidding").agg({"Purchase": "mean"})

df = pd.concat([df1, df2])

df.head()

df.groupby("Bidding").agg({"Purchase": "mean"})

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
 # HO = M1 = M2 ==> max bid ile ave .bidding arasında anlamlı bir farklılık yoktur
 # H1 = M1 != M2 ==> vardır.

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz
df.groupby("Bidding").agg({"Purchase": "mean"})


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

test_stat, pvalue = shapiro(df.loc[df["Bidding"] == "Maximum_Bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #p = 0,58 red edilemez
test_stat, pvalue = shapiro(df.loc[df["Bidding"] == "Average_Bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #p = 0,15 red edilemez

#varyans homejenliği
test_stat, pvalue = levene(df.loc[df["Bidding"] == "Maximum_Bidding", "Purchase"],
                           df.loc[df["Bidding"] == "Average_Bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p = 0,10 red edilemez.


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

test_stat, pvalue = ttest_ind(df.loc[df["Bidding"] == "Maximum_Bidding", "Purchase"],
                              df.loc[df["Bidding"] == "Average_Bidding", "Purchase"],
                              equal_var=True) #varyans hom sağlanmıyorsa false girecez.

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p = 0,34 red edilemez

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# ==> H0 hipotezi p < 0,05 olmadığı için Red edilemedi.İki grup arasında anlamlı bir fark yoktur diyebiliriz.



##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# ==> iki grupta da normallik varsayımı ve varyans homojenliği sağlandığı için "Bağımsız iki örneklem T testi" uygulanmıştır.
# ==> p-value değerleri 0,05 den büyük olduğu gözlenmiş böylece H0 hipotezi reddedilememiştir.


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# ==> purchase e göre yani "Tıklanan reklamlar sonrası satın alınan ürün sayısı" nda iki yöntem arasında istatistiki anlamda
# ==> anlamlı bir fark olmadığından müşteri istediği yöntemi seçebilir. tıklanma, etkileşim, kazanç ve dönüşüm oranlarındaki
# ==> farklılıklar değerlendirilip hangi yöntemin daha kazançlı olduğu tespit edilebilir.
# ==> iki grup gözlenmeye devam edilebilir.
# ==> Şimdilik iki yöntem arasındaki farklılık şans eseri ortaya çıkmıştır, diyebiliriz.

