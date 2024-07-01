# Mental Maps translator! :panda_face: :four_leaf_clover:	

This notebook is designed to translate MDL files to Python. The goal is to create a script that can automatically convert Causal Loop Diagrams into Adjacency Matrix, which can then be used for network analysis.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Trouble Shootings](#troubleshooting)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)


## Installation (virtual environment)

1. Clone the repository:

    ```bash
    [https://github.com/georgia-max/CldMaker.git](https://github.com/georgia-max/Phrame-MentalMaps.git)
    ```
2. Activate virtual environment in your terminal:
   ```
    source venv/bin/activate
    ```
3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Installation (conda)

To finetun the nlp models, you would need GPUs. This instllation guide is for setting up the environment to run on devices with GPUs. 
1. Clone the repository:

    ```bash
    [https://github.com/georgia-max/CldMaker.git](https://github.com/georgia-max/Phrame-MentalMaps.git)
    ```
2. Create a conda environment. 
2.1. Download Anaconda. 
2.2. Create a conda environment.
```
conda create --name myconda python3.11
```

2.3 Install the additional packages. 
```
pip install -r requirements_gpu.txt
```

Alternatively, install pytorch cuda based on your GPU version, and install the additional packages.. 



## Usage


## Example

Run the script in the terminal to translate a folder of Vensim MDL files and store them into .json files. 
```
./json_script.sh
```

Check out the Toy Example here: https://github.com/georgia-max/Phrame-MentalMaps/blob/master/Toy_Model.ipynb 

## Documentation

## Contributing to <Project_Name>
To contribute to <Project_Name>, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).


## License

This project uses the following license: [<license_name>](link).

