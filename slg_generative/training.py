# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_training.ipynb.

# %% auto 0
__all__ = ['Trainer']

# %% ../nbs/02_training.ipynb 3
from .models.vae import AutoEncoder
from .data.datasets import FashionMnistDataset
from torch.utils.data import DataLoader
from torch.optim import Adam
import torch.nn as nn
from tqdm import tqdm
import torch
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime

# %% ../nbs/02_training.ipynb 4
class Trainer:
    "Trainer for VAE models"

    def __init__(self,
        model:AutoEncoder, # Model
        train_dataloader:torch.utils.data.DataLoader, # Train Dataloader
        validation_dataloader:torch.utils.data.DataLoader, # Validation Dataloader
        loss_func:torch.nn.modules.loss._Loss, # Loss function
        optimizer:torch.optim.Optimizer, # Optimizer
        n_epochs:int, # Number of training epochs
        device:str # Device
    ):
        self.model = model
        self.train_dataloader = train_dataloader
        self.validation_dataloader = validation_dataloader
        self.loss_func = loss_func
        self.optimizer = optimizer
        self.n_epochs = n_epochs
        self.device = device
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.writer = SummaryWriter(f"runs/{self.timestamp}")

    def fit(self):
        # training loop
        running_loss = 0.
        last_loss = 0.
        n_batch_report = 100
        best_vloss = 1_000_000.

        for epoch in tqdm(range(self.n_epochs)):
            self.model.train(True)
            for batch_idx, (x, y) in enumerate(self.train_dataloader):
                x = x.to(self.device)
                self.optimizer.zero_grad()
                x_hat = self.model(x)
                loss = self.loss_func(x_hat, x)
                loss.backward()
                self.optimizer.step()
                
                if batch_idx % n_batch_report == (n_batch_report - 1):
                    print('\r Train Epoch: {}/{} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\r'.format(
                        epoch+1,
                        self.n_epochs,
                        batch_idx * len(x), 
                        len(self.train_dataloader.dataset),
                        n_batch_report * batch_idx / len(self.train_dataloader), 
                        loss.item()), 
                        end='')
                    sample_idx = epoch * len(self.train_dataloader) + batch_idx + 1
                    self.writer.add_scalar('Loss/train', loss.item(), sample_idx)
                    running_loss = 0

            self.model.train(False)
            running_vloss = 0.0
            for i, (x, y) in enumerate(self.validation_dataloader):
                x = x.to(self.device)
                x_hat = self.model(x)
                v_loss = self.loss_func(x_hat, x)
                running_vloss += v_loss.item()
            avg_vloss = running_vloss / (i + 1)
            print('\r Validion Loss: {}\r'.format(avg_vloss))
            self.writer.add_scalar('Loss/validation', avg_vloss, epoch + 1)
            self.writer.flush()

            if avg_vloss < best_vloss:
                best_vloss = avg_vloss
                model_path = f"runs/{self.timestamp}/model_{epoch+1}.pt"
                torch.save(self.model.state_dict(), model_path)


