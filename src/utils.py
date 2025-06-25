from PIL import Image
from torch.utils.data import Dataset

"""
    PREPARE THE DATASET:
    We need to: Load Images and labels, 
    convert them into the format TrOCR expects, 
    and batch them into a Dataset class

"""
class GoodnotesDataset(Dataset):
    # create a  constructor that contains a (list of file paths to the input images[e.g. handwriting images], the ground truth labels[strings], 
    def __init__(self, image_paths,texts,processor, max_target_length=128):
        # instances of the variables 
        self.image_paths = image_paths
        self.texts = texts
        self.processor = processor
        self.max_texts_length = max_target_length

    # this method is required in any custom torch.utils.data.Dataset || it tells how many samples are in your dataset
    # returns the number of training examples
    def __len__(self):
        return len(self.image_paths)


    def __getitem__(self, idx):

        image = Image.open(self.image_paths[idx]).convert("RGB")
        text = self.texts[idx]

        encoding = self.processor(
            images=image, text_target=text,
            padding="max_length", truncation=True,
            max_length=self.max_target_length,
            return_tensors="pt"
        )
        
        return {k: v.squeeze() for k, v in encoding.items()}