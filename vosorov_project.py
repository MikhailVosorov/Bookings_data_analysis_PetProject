#!/usr/bin/env python
# coding: utf-8

# Данные "/home/jupyter-m-vosorov/shared/homeworks/python_ds_miniprojects/2/bookings.csv"
# Задачи:
#     1. Пользователи из каких стран совершили наибольшее число успешных бронирований? Укажите топ-5.
#     2. На сколько ночей в среднем бронируют отели разных типов?
#     3. Иногда тип номера, полученного клиентом, отличается от изначально забронированного. Такое может произойти,
#        например, по причине овербукинга. Сколько подобных наблюдений встретилось в датасете?
#     4. На сколько ночей в среднем бронируют отели разных типов?
#             4.1 На какой месяц чаще всего успешно оформляли бронь в 2016?
#             4.2 Изменился ли самый популярный месяц в 2017? 
#             4.3 На какой месяц бронирования отеля типа City Hotel отменялись чаще всего в 2015, 2016, 2017?
#     5. Посмотрите на числовые характеристики трёх переменных: adults, children и babies.
#        Какая из них имеет наибольшее среднее значение?
#     6. Создайте колонку total_kids, объединив children и babies. Для отелей какого типа среднее значение переменной оказалось          наибольшим?
#     7. Создайте переменную has_kids, которая принимает значение True, если клиент при бронировании указал хотя бы одного                ребенка, в противном случае – False. Посчитайте отношение количества ушедших пользователей к общему количеству клиентов,        выраженное в процентах (churn rate). Укажите, среди какой группы показатель выше.

# In[15]:


import pandas as pd
bookings = pd.read_csv("/home/jupyter-m-vosorov/shared/homeworks/python_ds_miniprojects/2/bookings.csv", sep = ";")
bookings.columns = bookings.columns.str.lower().str.replace(" ", "_")
# Читай данные и переименовываю названия колонок для более удобной работы с ними
bookings.head()


# In[18]:


# Задача №1
bookings.query("is_canceled == 0").country.value_counts()[:5]


# In[25]:


# Задача №2
bookings     .groupby("hotel", as_index = False)     .agg({"stays_total_nights" : "mean"})     


# In[28]:


# Задача №3
bookings.query("reserved_room_type != assigned_room_type").assigned_room_type.count()


# In[33]:


# Задача №4.1
bookings     .query("arrival_date_year == 2016")     .arrival_date_month.value_counts()[:1]


# In[34]:


# Задача №4.2
bookings     .query("arrival_date_year == 2017")     .arrival_date_month.value_counts()[:1]


# In[51]:


# Задча №4.3
bookings     .query("is_canceled == 1 and hotel == 'City Hotel' ")     .groupby(["arrival_date_year", "arrival_date_month"])     .agg({"arrival_date_month" : "count"})     


# In[52]:


# Задача №5
bookings.describe()
# Ответ: adults


# In[53]:


# Задача №6
bookings["total_kids"] = bookings.children + bookings.babies
bookings     .groupby("hotel", as_index = False)     .agg({"total_kids" : "mean"})
# Ответ: Resort Hotel


# In[78]:


# Задача №7
bookings["has_kids"] = bookings.total_kids > 0
churn_rate_with_children_df = bookings                            .query("has_kids == True")                            .is_canceled.value_counts()
churn_rate_with_children = churn_rate_with_children_df[1] / (churn_rate_with_children_df[0] + churn_rate_with_children_df[1])

churn_rate_without_children_df = bookings                            .query("has_kids == False")                            .is_canceled.value_counts()
churn_rate_without_children = churn_rate_without_children_df[1] / (churn_rate_without_children_df[0] + churn_rate_without_children_df[1])

print("Churn rate in group of people with kids is", round(churn_rate_with_children, 4) * 100)
print("Churn rate in group of people without kids is", round(churn_rate_without_children, 4) * 100)


# In[ ]:




