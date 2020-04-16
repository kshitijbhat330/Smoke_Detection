import sys
import torch
from sklearn.metrics import cohen_kappa_score, confusion_matrix, f1_score
from Models.SmokeNet import SmokeNet, predict
from Models.SmokeDataset import get_datasets

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class_weights, training_data, validation_data, testing_data = get_datasets()

variant = sys.argv[1]
fname = sys.argv[2]
model = SmokeNet(variant)
model.load_state_dict(torch.load(fname)["model_state_dict"])
model.to(device)

y_pred = predict(model, testing_data)
y_pred = torch.stack(y_pred)
y_pred = torch.argmax(y_pred, axis=1).tolist()
y_true = [testing_data[i][1].item() for i in range(len(testing_data))]

print("The cohen kappa score: ", cohen_kappa_score(y_true, y_pred))
print("The f1_score score: ", f1_score(y_true, y_pred, average="macro"))
print("The confusion matrix:")
print(confusion_matrix(y_true, y_pred))
