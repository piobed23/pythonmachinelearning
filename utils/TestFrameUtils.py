import pytest
import pandas as pd
from datetime import datetime

class TestFrameUtils:
    def test_prepare_data_frame_creates_time_features(self):
        df = pd.DataFrame({
            'date_ist': ['15/01/2025', '15/01/2025'],
            'time_ist': ['09:30', '18:45'],
            'pm2_5': [45.2, 78.9]
        })
        result = FrameUtils.prepare_data_frame(df)
        assert result['hour'].tolist() == [9, 18]
        assert result['is_rush_hour'].tolist() == [1, 1]
        assert result['is_night'].tolist() == [0, 0]

    def test_prepare_data_frame_creates_lag_features(self):
        df = pd.DataFrame({
            'date_ist': ['15/01/2025'] * 5,
            'time_ist': ['08:00', '09:00', '10:00', '11:00', '12:00'],
            'pm2_5': [10, 20, 30, 40, 50]
        })
        result = FrameUtils.prepare_data_frame(df)
        assert pd.isna(result.loc[0, 'pm25_lag_1'])
        assert result.loc[2, 'pm25_lag_1'] == 20
        assert result.loc[3, 'pm25_lag_3'] == 10

    def test_drop_columns_removes_specified_columns(self):
        df = pd.DataFrame({
            'pm10': [50], 'aqi_index': [100], 'date_ist': ['15/01/2025'],
            'time_ist': ['09:00'], 'description': ['hazy'], 'condition_text': ['smoke'],
            'pm2_5': [45], 'lat': [28.6], 'lon': [77.2], 'hour': [9]
        })
        result = FrameUtils.drop_columns(df)
        assert list(result.columns) == ['hour']
        assert len(result) == 1