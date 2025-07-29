from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

class OnlineAnomalyModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(n_estimators=100, contamination=0.01)
        self.data = []
        self.fitted = False

    def add_data_point(self, r, s):
        try:
            r_val = float(r)
            s_val = float(s)
            self.data.append([r_val, s_val])
            if len(self.data) > 1000:
                self.data.pop(0)
            if len(self.data) >= 100 and not self.fitted:
                self.train()
        except Exception as e:
            logging.warning(f"Failed to add data point: {e}")

    def train(self):
        if len(self.data) < 10:
            logging.warning("Not enough data to train")
            return
        scaled = self.scaler.fit_transform(self.data)
        self.model.fit(scaled)
        self.fitted = True
        logging.info("Model trained on latest data")

    def predict(self, r, s):
        if not self.fitted:
            return False
        try:
            point = np.array([[float(r), float(s)]])
            scaled = self.scaler.transform(point)
            prediction = self.model.predict(scaled)
            return prediction[0] == -1  # -1 = anomali
        except:
            return False