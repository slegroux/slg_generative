# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/00_data.datasets.ipynb.

# %% auto 0
__all__ = ['ImageDataset', 'MnistDataset', 'FashionMnistDataset']

# %% ../../nbs/00_data.datasets.ipynb 3
import pandas as pd
import torchvision
from torch.utils.data import Dataset, DataLoader
import torch
from matplotlib import pyplot as plt


# %% ../../nbs/00_data.datasets.ipynb 5
class ImageDataset(Dataset):
    " Base class for image datasets providing visualization of (image, label) samples"

    def show(self,
        index:int # Index of the (image,label) sample to visualize
        ):
        X, y = self.__getitem__(index)
        plt.figure(figsize = (1, 1))
        plt.imshow(X.numpy().reshape(28,28),cmap='gray')
        plt.title(f"Label: {int(y)}")
        plt.show()

# %% ../../nbs/00_data.datasets.ipynb 6
class MnistDataset(ImageDataset):
    "MNIST digit dataset"

    def __init__(self,
        data_root:str='./data' # Path to data root folder
        ):
        super().__init__()
        self.ds = torchvision.datasets.MNIST(
            data_root,
            transform=torchvision.transforms.ToTensor(), 
            download=True
        )
    def __len__(self):
        return len(self.ds)
    
    def __getitem__(self, idx):
        x = self.ds[idx][0].squeeze(0).flatten()
        return x, self.ds.targets[idx]

# %% ../../nbs/00_data.datasets.ipynb 8
class FashionMnistDataset(ImageDataset):
    "Fashion MNIST Dataset"
    
    def __init__(self, 
        csv_file:str # Path to csv data file
        ):
        super().__init__()
        # read csv
        self.train = pd.read_csv(csv_file)
        # normalize data
        X = self.train.iloc[:,1:].values / 255.
        X = (X-0.5)/0.5
        Y = self.train.iloc[:,0].values
        # convert X to FloatTensor & Y to LongTensor
        self.X, self.Y = torch.tensor(X, dtype=torch.float32) , torch.tensor(Y, dtype=torch.int64)
    
    def __len__(self):
        return len(self.train)

    def __getitem__(self, idx):
        return (self.X[idx],  self.Y[idx])
