import json
import torch
import pandas as pd
from tqdm import tqdm


def train_model(model, data_loader, optimizer, training_params):
    model.train()
    train_loss = 0

    tk = tqdm(data_loader, total=len(data_loader))
    for data in tk:
        for key, value in data.items():
            data[key] = value.to(training_params.device)

        optimizer.zero_grad()
        _, loss = model(**data)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    return train_loss / len(data_loader)


def evaluate_model(model, data_loader, training_params):
    model.eval()
    test_loss = 0
    test_preds = []

    with torch.no_grad():
        tk = tqdm(data_loader, total=len(data_loader))
        for data in tk:
            for key, value in data.items():
                data[key] = value.to(training_params.device)

            batch_preds, loss = model(**data)
            test_loss += loss.item()
            test_preds.append(batch_preds)

    return test_preds, test_loss / len(data_loader)


def save_model(model, output_model_path):
    torch.save(model, output_model_path)


def save_metrics(metrics, output_metrics_path):
    with open(output_metrics_path, "w") as metrics_file:
        json.dump(metrics, metrics_file)


def save_predictions(test_orig_targets, test_decoded_preds, output_predictions_path):
    df = pd.DataFrame(
        {
            "test_orig_targets": test_orig_targets,
            "test_decoded_preds": test_decoded_preds,
        }
    )

    df.to_csv(output_predictions_path, index=False)
