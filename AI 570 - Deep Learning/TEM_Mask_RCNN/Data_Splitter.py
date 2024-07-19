def create_split_directories(base_dir, categories):
    """Creates the directory structure for putting images into train, validation, and test groups.
    
    Args:
        base_dir (str): The base directory where the data will be stored.
        categories (list): A list of the categories in the dataset
        
    Returns:
        None
            
    """
    for split in ['train', 'validation', 'test']:
        for category in categories:
            new_path = os.path.join(base_dir, split, category)
            if not os.path.exists(new_path):
                os.makedirs(path, exist_ok=True)

split_base_dir = './dataset_split'
#create_split_directories(split_base_dir, categories)

# Function to split and move images
def split_data(base_dir, split_base_dir, categories, train_size=0.7, validation_size=0.15):
    """
    Split the data into train, validation, and test sets and then moves the 
    image files to the appropriate directories.

    Args:
        base_dir (str): The base directory where the data is stored.
        split_base_dir (str): The base directory where the split data will be stored.
        categories (list): A list of the categories in the dataset.
        train_size (float): The proportion of the data to include in the train split.
        validation_size (float): The proportion of the data to include in the validation split.
                                The remainder will go into the test split

    Returns:
        None
    
    """
        
    for category in categories:
        category_path = os.path.join(base_dir, category)
        images = os.listdir(category_path) # Lists the files in the directory
        train, test = train_test_split(images, train_size=train_size, random_state=RANDOM_STATE) # test here is the 
                                                                                            # validation and test split
        val, test = train_test_split(test, test_size=validation_size / (1 - train_size), random_state=RANDOM_STATE)
        
        for img in train:
            shutil.copy(os.path.join(category_path, img), os.path.join(split_base_dir, 'train', category, img))
        for img in val:
            shutil.copy(os.path.join(category_path, img), os.path.join(split_base_dir, 'validation', category, img))
        for img in test:
            shutil.copy(os.path.join(category_path, img), os.path.join(split_base_dir, 'test', category, img))

#split_data(base_path, split_base_dir, categories)   # Uncomment this to create the splits