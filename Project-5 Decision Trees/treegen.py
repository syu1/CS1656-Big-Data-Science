from id3 import Id3Estimator, export_text
# download from https://svaante.github.io/decision-tree-id3/index.html
import numpy as np

new_feature_names = ["day_of_week",
                 "fruit",
                 "color"]

XX = np.array([["mon", "blueberries", "blue"],
              ["mon", "blueberries", "green"],
              ["mon", "blueberries", "blue"],
              ["tue", "blueberries", "black"],
              ["wed", "blueberries", "green"],
              ["mon", "blueberries", "red"],
 
              ["mon", "grapes", "black"],
              ["mon", "grapes", "red"],
              ["mon", "grapes", "green"],
              ["tue", "grapes", "green"],
              ["mon", "grapes", "blue"]])

yy = np.array(["good","bad","good","bad","bad","bad",
               "bad","good","good","good","bad"])

clf = Id3Estimator()
clf.fit(XX, yy, check_input=True)

print(export_text(clf.tree_, new_feature_names))
