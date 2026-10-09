import pandas as pd


# ============================================================
# 讀取資料
# ============================================================

df = pd.read_csv("T_ONTIME_REPORTING.csv")

# 查看前五筆資料
# print(df.head())

# 查看資料大小
print("Original Size: ", df.shape)

# 查看欄位名稱
# print(df.columns.tolist())

# 查看各欄位資料型態
# print(df.dtypes)


# ============================================================
# 轉換資料型態
# ============================================================

df["FL_DATE"] = pd.to_datetime(
    df["FL_DATE"],
    format="mixed"
)

# 檢查日期欄位資料型態
# print(df["FL_DATE"].dtype)


# ============================================================
# 檢查重複值與缺失值
# ============================================================

# 檢查完全重複的資料筆數
# print("Duplicate rows:", df.duplicated().sum())

# 檢查各欄位缺失值數量
# print(df.isna().sum())


# ============================================================
# 建立 ORD 出發與抵達樣本
# ============================================================

# 出發樣本：
# 保留從 ORD 出發、未取消且有出發延誤資料的航班。
# 不排除 diverted flights，因為這些航班仍可能具有有效的 ORD 出發資料。

ord_dep = df[
    (df["ORIGIN"] == "ORD") &
    (df["CANCELLED"] == 0) &
    (df["DEP_DELAY"].notna())
].copy()


# 抵達樣本：
# 保留目的地為 ORD、未取消、未轉降且有抵達延誤資料的航班。

ord_arr = df[
    (df["DEST"] == "ORD") &
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()


# 查看出發與抵達樣本大小
# print("Departure sample:", ord_dep.shape)
# print("Arrival sample:", ord_arr.shape)


# ============================================================
# 檢查數值與可能的資料異常
# ============================================================

# 負的 delay 代表提早出發或抵達，因此不視為錯誤。
# 極端 delay 沒有證據顯示為資料輸入錯誤，因此保留。

# 查看出發延誤的描述統計
# print(ord_dep["DEP_DELAY"].describe())

# 查看抵達延誤的描述統計
# print(ord_arr["ARR_DELAY"].describe())

# 查看出發延誤的分位數
# print(
#     ord_dep["DEP_DELAY"].quantile(
#         [0, 0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]
#     )
# )

# 查看抵達延誤的分位數
# print(
#     ord_arr["ARR_DELAY"].quantile(
#         [0, 0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]
#     )
# )

# 檢查是否存在負的 TAXI_OUT
# print("Negative TAXI_OUT:", (ord_dep["TAXI_OUT"] < 0).sum())

# 檢查是否存在負的 TAXI_IN
# print("Negative TAXI_IN:", (ord_arr["TAXI_IN"] < 0).sum())

# 檢查出發樣本是否存在非正的 DISTANCE
# print(
#     "Non-positive departure DISTANCE:",
#     (ord_dep["DISTANCE"] <= 0).sum()
# )

# 檢查抵達樣本是否存在非正的 DISTANCE
# print(
#     "Non-positive arrival DISTANCE:",
#     (ord_arr["DISTANCE"] <= 0).sum()
# )


# ============================================================
# 建立 ORD Scheduled Traffic
# ============================================================

# 使用原始資料計算 scheduled traffic。
# 即使航班之後取消或轉降，仍屬於原先排定的機場需求。

# 計算各日期與出發時段的 scheduled departures
scheduled_dep = (
    df[df["ORIGIN"] == "ORD"]
    .groupby(["FL_DATE", "DEP_TIME_BLK"])
    .size()
    .reset_index(name="SCHEDULED_DEPARTURES")
    .rename(columns={"DEP_TIME_BLK": "TIME_BLK"})
)


# 計算各日期與抵達時段的 scheduled arrivals
scheduled_arr = (
    df[df["DEST"] == "ORD"]
    .groupby(["FL_DATE", "ARR_TIME_BLK"])
    .size()
    .reset_index(name="SCHEDULED_ARRIVALS")
    .rename(columns={"ARR_TIME_BLK": "TIME_BLK"})
)


# 合併 scheduled departures 與 scheduled arrivals
airport_traffic = pd.merge(
    scheduled_dep,
    scheduled_arr,
    on=["FL_DATE", "TIME_BLK"],
    how="outer"
)


# Outer merge 後的缺失值代表該時段沒有 scheduled departure 或 arrival。
# 將航班數量補為 0，並轉為整數。

traffic_count_columns = [
    "SCHEDULED_DEPARTURES",
    "SCHEDULED_ARRIVALS"
]

airport_traffic[traffic_count_columns] = (
    airport_traffic[traffic_count_columns]
    .fillna(0)
    .astype(int)
)


# 建立總 scheduled traffic 作為 congestion measure
airport_traffic["TOTAL_SCHEDULED_TRAFFIC"] = (
    airport_traffic["SCHEDULED_DEPARTURES"]
    + airport_traffic["SCHEDULED_ARRIVALS"]
)


# 查看 airport traffic 前五筆資料
# print(airport_traffic.head())

# 查看 airport traffic 資料大小
# print(airport_traffic.shape)

# 查看 scheduled traffic 描述統計
# print(
#     airport_traffic[
#         [
#             "SCHEDULED_DEPARTURES",
#             "SCHEDULED_ARRIVALS",
#             "TOTAL_SCHEDULED_TRAFFIC"
#         ]
#     ].describe()
# )

# 檢查日期與時段組合是否重複
# print(
#     "Duplicate date/time blocks:",
#     airport_traffic.duplicated(
#         subset=["FL_DATE", "TIME_BLK"]
#     ).sum()
# )


# ============================================================
# 將 Scheduled Traffic 合併至出發樣本
# ============================================================

# 使用 scheduled departure time block 配對 congestion。
# 保留原始 DEP_TIME_BLK 欄位名稱。

ord_dep = pd.merge(
    ord_dep,
    airport_traffic,
    left_on=["FL_DATE", "DEP_TIME_BLK"],
    right_on=["FL_DATE", "TIME_BLK"],
    how="left"
)

# TIME_BLK 與 DEP_TIME_BLK 重複，因此移除
ord_dep = ord_dep.drop(columns=["TIME_BLK"])


# ============================================================
# 將 Scheduled Traffic 合併至抵達樣本
# ============================================================

# 使用 scheduled arrival time block 配對 congestion。
# 保留原始 ARR_TIME_BLK 欄位名稱。

ord_arr = pd.merge(
    ord_arr,
    airport_traffic,
    left_on=["FL_DATE", "ARR_TIME_BLK"],
    right_on=["FL_DATE", "TIME_BLK"],
    how="left"
)

# TIME_BLK 與 ARR_TIME_BLK 重複，因此移除
ord_arr = ord_arr.drop(columns=["TIME_BLK"])


# ============================================================
# 最終資料檢查
# ============================================================

# 查看最終出發與抵達資料大小
# print("Departure shape:", ord_dep.shape)
# print("Arrival shape:", ord_arr.shape)


# 檢查出發樣本是否全部從 ORD 出發
# print(
#     "Non-ORD departure origins:",
#     (ord_dep["ORIGIN"] != "ORD").sum()
# )

# 檢查出發樣本是否包含取消航班
# print(
#     "Cancelled departure flights:",
#     (ord_dep["CANCELLED"] != 0).sum()
# )

# 檢查抵達樣本是否全部以 ORD 為目的地
# print(
#     "Non-ORD arrival destinations:",
#     (ord_arr["DEST"] != "ORD").sum()
# )

# 檢查抵達樣本是否包含取消航班
# print(
#     "Cancelled arrival flights:",
#     (ord_arr["CANCELLED"] != 0).sum()
# )

# 檢查抵達樣本是否包含 diverted flights
# print(
#     "Diverted arrival flights:",
#     (ord_arr["DIVERTED"] != 0).sum()
# )


# 檢查 DEP_DEL15 是否與 DEP_DELAY >= 15 的定義一致
# print(
#     "DEP_DEL15 mismatches:",
#     (
#         ord_dep["DEP_DEL15"]
#         != (ord_dep["DEP_DELAY"] >= 15).astype(int)
#     ).sum()
# )

# 檢查 ARR_DEL15 是否與 ARR_DELAY >= 15 的定義一致
# print(
#     "ARR_DEL15 mismatches:",
#     (
#         ord_arr["ARR_DEL15"]
#         != (ord_arr["ARR_DELAY"] >= 15).astype(int)
#     ).sum()
# )


# 檢查出發樣本的 TOTAL_SCHEDULED_TRAFFIC 計算是否一致
# print(
#     "Departure congestion mismatches:",
#     (
#         ord_dep["TOTAL_SCHEDULED_TRAFFIC"]
#         != (
#             ord_dep["SCHEDULED_DEPARTURES"]
#             + ord_dep["SCHEDULED_ARRIVALS"]
#         )
#     ).sum()
# )

# 檢查抵達樣本的 TOTAL_SCHEDULED_TRAFFIC 計算是否一致
# print(
#     "Arrival congestion mismatches:",
#     (
#         ord_arr["TOTAL_SCHEDULED_TRAFFIC"]
#         != (
#             ord_arr["SCHEDULED_DEPARTURES"]
#             + ord_arr["SCHEDULED_ARRIVALS"]
#         )
#     ).sum()
# )


# 定義出發分析需要的主要變數
departure_required_variables = [
    "FL_DATE",
    "DAY_OF_WEEK",
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "CRS_DEP_TIME",
    "DEP_TIME_BLK",
    "DEP_DELAY",
    "DEP_DEL15",
    "DISTANCE",
    "SCHEDULED_DEPARTURES",
    "SCHEDULED_ARRIVALS",
    "TOTAL_SCHEDULED_TRAFFIC"
]

# 檢查出發分析主要變數是否存在缺失值
# print(
#     ord_dep[
#         departure_required_variables
#     ].isna().sum()
# )


# 定義抵達分析需要的主要變數
arrival_required_variables = [
    "FL_DATE",
    "DAY_OF_WEEK",
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "CRS_ARR_TIME",
    "ARR_TIME_BLK",
    "ARR_DELAY",
    "ARR_DEL15",
    "DISTANCE",
    "SCHEDULED_DEPARTURES",
    "SCHEDULED_ARRIVALS",
    "TOTAL_SCHEDULED_TRAFFIC"
]

# 檢查抵達分析主要變數是否存在缺失值
# print(
#     ord_arr[
#         arrival_required_variables
#     ].isna().sum()
# )


# 檢查最終出發資料是否有完全重複的資料
# print(
#     "Duplicate departure rows:",
#     ord_dep.duplicated().sum()
# )

# 檢查最終抵達資料是否有完全重複的資料
# print(
#     "Duplicate arrival rows:",
#     ord_arr.duplicated().sum()
# )

# ============================================================
# 輸出處理後的資料
# ============================================================

ord_dep.to_csv("ord_departure_dataset.csv", index=False)
ord_arr.to_csv("ord_arrival_dataset.csv", index=False)

# 確認輸出資料的大小
print("Departure:", ord_dep.shape)
print("Arrival:", ord_arr.shape)