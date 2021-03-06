"""
The primary function here combines and filters the CIFAR datasets.
It also takes a batch number as an input and feeds it to the dataloader.
"""

import torch
import torchvision
import torchvision.transforms as transforms
import Resources.helpers as helpers


def load_vehicles(batch_num):
    """
    # For converting data into normalised grayscale tensors in the range [-1,1].
    transformer_test = transforms.Compose([transforms.Grayscale(1), transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    transformer_train = transforms.Compose([transforms.Grayscale(1), transforms.RandomResizedCrop(32), transforms.RandomHorizontalFlip(),
                                            transforms.ToTensor(), transforms.Normalize((0.5,),(0.5,))])
    """
    #3-channel transformations
    transformer_test = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))])
    transformer_train = transforms.Compose([transforms.RandomResizedCrop(32), transforms.RandomHorizontalFlip(),
                                            transforms.ToTensor(), transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])

    

    # Obtaining CIFAR-10 and CIFAR-100
    training_set10 = torchvision.datasets.CIFAR10(root='./data', train=True, transform=transformer_train,download=False)  # change to true if required.
    testing_set10 = torchvision.datasets.CIFAR10(root='./data', train=False, transform=transformer_train, download=False)
    training_set100 = torchvision.datasets.CIFAR100(root='./data', train=True, transform=transformer_test, download=False)
    testing_set100 = torchvision.datasets.CIFAR100(root='./data', train=False, transform=transformer_test, download=False)

    # Filtering classes and merging data from both CIFAR sets.
    training_set10 = torch.utils.data.Subset(training_set10, helpers.item_retriever(training_set10, True))
    training_set100 = torch.utils.data.Subset(training_set100, helpers.item_retriever(training_set100, False))
    training_set = torch.utils.data.ConcatDataset([training_set10, training_set100])

    testing_set10 = torch.utils.data.Subset(testing_set10, helpers.item_retriever(testing_set10, True))
    testing_set100 = torch.utils.data.Subset(testing_set100, helpers.item_retriever(testing_set100, False))
    testing_set = torch.utils.data.ConcatDataset([testing_set10, testing_set100])

    #loading data
    training_loader = torch.utils.data.DataLoader(training_set, batch_size=batch_num, shuffle=True)
    testing_loader = torch.utils.data.DataLoader(testing_set, batch_size=batch_num)
    
    return (training_loader, testing_loader)
