# Lettres en Lumière - LLM based OCR text correction

This repository contains the code for the OCR text correction using a LLM.

## Repository structure

- `src/` contains the source code for the utils library
- `notebooks/` contains the notebooks used for the experiments
- `models/` contains the output models

## Environment setup

To setup the environment using conda (recommended):

```bash
conda create -n lel-llm
conda activate lel-llm
conda install pytorch torchvision torchaudio transformers datasets jiwer ipykernel accelerate matplotlib pytorch-cuda=12.3 -c pytorch -c nvidia -c conda-forge
```

If using pip:

```bash
pip install -r requirements.txt
```

## Usage

You can modify the VARIABLES on top of both `training.ipynb` and `evaluation.ipynb` to change the parameters.
The base parameters are set to demo using the huggingface `wikipedia` dataset.

### Training

- To train the model, run the `training.ipynb` notebook.
- After training, the model will be saved in the `models/` directory.

### Evaluation

- To evaluate the model, run the `evaluation.ipynb` notebook.
- To use the previously trained model, set the `MODEL_PATH` variable to the path of the model in the `models/` directory (you also need to add the checkpoint in the path). e.g. `llm-wikipedia/checkpoint-1000`.
- Make sure to set the tokenizer and system prompt to the same used in training.
- The evaluation will output the WER and CER (with std) of the model.
- It also shows some examples of the model's predictions.

