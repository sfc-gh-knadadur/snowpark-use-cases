# this class will be used in our sproc
# needs to be redone to use snowflake instead of pandas
# this class will be used in our sproc
# needs to be redone to use snowflake instead of pandas
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from pytorch_forecasting.data import (  # GroupNormalizer,
    NaNLabelEncoder,
    TimeSeriesDataSet,
)

class snowflakeDataLoader:
    def __init__(self, data, min_dates = 30, top_k = 1000):
        self.data=data.copy()
        self.min_dates = min_dates
        self.top_k = top_k
        self._filter_upcs()
        self._create_date_features()

    def _filter_upcs(self):
        full_asins = (
            self.data[["amazon_id", "ordered_date", "search_spend"]]
            .groupby("amazon_id")
            .agg({"search_spend": "sum", "ordered_date": "count"})
            .reset_index()
            .sort_values("search_spend", ascending=False)
        )
        full_asins = full_asins[full_asins["ordered_date"] > self.min_dates]
        full_asins = full_asins.head(self.top_k)
        full_asins = full_asins["amazon_id"].tolist()
        print(f"using {len(full_asins)} ASINs")
        self.data = self.data[self.data["amazon_id"].isin(full_asins)]

    def _create_date_features(self):
        self.data["date"] = pd.to_datetime(self.data["ordered_date"])
        cal = calendar()
        holidays = cal.holidays(start=self.data.date.min(), end=self.data.date.max())
        self.data["holiday"] = self.data["date"].isin(holidays).astype("string").astype("category")

        self.data["quarter"] = self.data.date.dt.quarter.astype("string").astype("category")
        self.data["month"] = self.data.date.dt.month.astype("string").astype("category")
        self.data["day"] = self.data.date.dt.day.astype("string").astype("category")
        self.data["weekend"] = (self.data.date.dt.weekday >= 5).astype("string").astype("category")
        
        # creating 7-day lagged past columns
        self.data["online_units_past"] = self.data["online_units"].shift(7)
        self.data["rep_oos_past"] = self.data["rep_oos"].shift(7)
        self.data["order_revenue_past"] = self.data["order_revenue"].shift(7)
        self.data["average_sales_price_past"] = self.data["average_sales_price"].shift(7)
        self.data["search_spend_past"] = self.data["search_spend"].shift(7)
        
        # extra past columns
        self.data["price_discount_past"] = self.data["price_discount"].shift(7)
        self.data["best_deal_past"] = self.data["best_deal"].shift(7)
        self.data["promo_code_past"] = self.data["promo_code"].shift(7)
        self.data["discount_price_past"] = self.data["discount_price"].shift(7)
        
        self.data = self.data.dropna()
        
        # make asp_by_prod and price_index cols
        index_cols = ["amazon_id", "pepsi_brand", "category", "sub_category", "business_unit", "sub_business_unit" ]
        
        # aggregate by the index_cols and calculate the mean of "average_sales_price"
        grouped_df = self.data.groupby(index_cols)["average_sales_price"].mean().reset_index()

        # merge with self.data on index columns
        merged_df = pd.merge(grouped_df, self.data, on=index_cols, how="inner")
        self.data = merged_df

        # rename the "average_sales_price_x" column to "asp_by_prod"
        self.data = self.data.rename(columns={"average_sales_price_x": "asp_by_prod"})
        self.data = self.data.rename(columns={"average_sales_price_y": "average_sales_price"})
        
        # price_index
        self.data["price_index"] = self.data["average_sales_price"] / self.data["asp_by_prod"]

        self.data = self.data.reset_index(drop=True)

        min_date = self.data["date"].min()

        self.data["time_idx"] = (self.data["date"] - min_date).dt.days

    def __call__(
        self, min_prediction_length, max_prediction_length, min_encoder_length, max_encoder_length, batch_size, num_workers
    ):
        data = self.data.copy()
        data["rep_oos_past"] = data["rep_oos_past"].fillna(0)
        data["rep_oos"] = data["rep_oos"].fillna(0)
        data["amazon_id"] = data["amazon_id"].astype(str).astype("category")
        data["pepsi_brand"] = data["pepsi_brand"].astype(str).astype("category")
        data["business_unit"] = data["business_unit"].astype(str).astype("category")
        data["sub_business_unit"] = data["sub_business_unit"].astype(str).astype("category")
        data["category"] = data["category"].astype(str).astype("category")
        data["sub_category"] = data["sub_category"].astype(str).astype("category")

        print(f"{data.shape}")

        max_time_idx = data["time_idx"].max()
        training_cutoff = max_time_idx - max_prediction_length

        print(f"{max_time_idx}")
        print(f"{training_cutoff=}")

        self.dataset = TimeSeriesDataSet(
            data[lambda x: x.time_idx <= training_cutoff],
            time_idx="time_idx",
            target="order_revenue",
            group_ids=["amazon_id"],
            min_encoder_length=min_encoder_length,
            max_encoder_length=max_encoder_length,
            min_prediction_length=min_prediction_length,
            max_prediction_length=max_prediction_length,
            categorical_encoders={
                "amazon_id": NaNLabelEncoder().fit(data.amazon_id),
                "pepsi_brand": NaNLabelEncoder().fit(data.pepsi_brand),
                "business_unit": NaNLabelEncoder().fit(data.business_unit),
                "sub_business_unit": NaNLabelEncoder().fit(data.sub_business_unit),
                "category": NaNLabelEncoder().fit(data.category),
                "sub_category": NaNLabelEncoder().fit(data.sub_category),
            },
            static_categoricals=[
                "amazon_id",
                "pepsi_brand",
                "business_unit",
                "sub_business_unit",
                "category",
                "sub_category",
                
            ],
            time_varying_known_categoricals=[
                "holiday",
                "quarter",
                "month",
                "day",
                "weekend",
            ],
            time_varying_unknown_reals=[
                "online_units",
                "average_sales_price",
                "online_units_past",
                "average_sales_price_past",
                "price_index",
                "rep_oos",
                "rep_oos_past",
                "order_revenue_past",
            ],
            time_varying_known_reals=["search_spend", "search_spend_past"],
            add_relative_time_idx=True,
            add_target_scales=False,
            add_encoder_length=True,
            allow_missing_timesteps=True,
        )

        print("Time series params: ", self.dataset.get_parameters())
        self.dataframe = data

        validation = TimeSeriesDataSet.from_dataset(
            self.dataset, data, predict=True, stop_randomization=True
        )
        self.train_dataloader = self.dataset.to_dataloader(
            train=True, batch_size=batch_size, num_workers=num_workers
        )
        self.val_dataloader = validation.to_dataloader(
            train=False, batch_size=batch_size, num_workers=num_workers
        )