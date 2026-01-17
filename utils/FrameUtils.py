import pandas as pd


class FrameUtils:
    @staticmethod
    def prepare_data_frame(data_frame: pd.DataFrame):
        df = data_frame.copy()
        df['hour'] = pd.to_datetime(df['time_ist'], format='%H:%M').dt.hour
        df['date_ist'] = pd.to_datetime(df['date_ist'], format='%d/%m/%Y')

        df = df.sort_values(['date_ist', 'hour']).reset_index(drop=True)

        df['day_of_week'] = df['date_ist'].dt.dayofweek
        df['is_rush_hour'] = df['hour'].isin([8, 9, 10, 17, 18, 19, 20, 21, 22]).astype(int)
        df['is_night'] = df['hour'].isin([23, 0, 1, 2, 3, 4, 5, 6]).astype(int)
        df['pm25_lag_1'] = df['pm2_5'].shift(1)  # 1 hour ago
        df['pm25_lag_2'] = df['pm2_5'].shift(2)  # 2 hours ago
        df['pm25_lag_3'] = df['pm2_5'].shift(3)  # 3 hours ago
        df['pm25_lag_24'] = df['pm2_5'].shift(24)

        return df

    @staticmethod
    def drop_columns(dataFrame: pd.DataFrame):
        return dataFrame.drop([
            'pm10', 'aqi_index', 'date_ist', 'time_ist',
            'description', 'condition_text', 'pm2_5', 'lat', 'lon'
        ], axis=1)
