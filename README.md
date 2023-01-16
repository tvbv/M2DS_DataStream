# Stock forecasting with stream-learning neural networks

This project is a team project for the Data Stream Processing's course at Ecolze Polytechnique. 
The goal is to predict the stock market using stream-learning neural networks.

## Table of contents

- [Authors](#authors)
- [Getting started](#getting-started)
  - [Clone the repository](#clone-the-repository)
  - [Prerequisites](#prerequisites)
  - [Run the project](#run-the-project)
    - [1. Zookeeper](#1-zookeeper)
    - [2. Kafka](#2-kafka)
    - [3. model_training_continual.py](#3-model_training_continualpy)
    - [4. dataset_handler.py](#4-dataset_handlerpy)
    - [5. rolling_prediction.py](#5-rolling_predictionpy)
    - [6. stock_mock_API.py](#6-stock_mock_APIpy)
  - [Results](#results)
  - [References](#references)

## Authors

* **BERSANI--VERONI Thomas** [thomas.bersani--veroni@ens-paris-saclay.fr](thomas.bersani--veroni@ens-paris-saclay.fr)
* **GENSBITTEL Luc** [luc.gensbittel@polytechnique.edu](luc.gensbittel@polytechnique.edu)
* **LERMITE Titouan** [titouan.lermite@polytechnique.edu](titouan.lermite@polytechnique.edu)

## Getting Started

### Clone the repository

To clone the repository, run the following command:

```bash
git clone https://github.com/TitouanLMT/M2DS_DataStream/tree/main
```

### Prerequisites

The requirements are in the [requirements.txt](requirements.txt) file. You can install them with the following command:

```
pip install -r requirements.txt
```

### Run the project

This part assumes you are running the commands in seperate terminals.

#### 1. Zookeeper

To run the project, you need to run a Zookeeper server. To do so, run the following command, assuming you are
in the correct Zookeeper directory:

```
zookeeper-server-start.sh config/zookeeper.properties
```

#### 2. Kafka

To run the project, you need to run a Kafka server. To do so, run the following command, assuming you are
in the correct Kafka directory:

```
kafka-server-start.sh config/server.properties
```

#### 3. [model_training_continual.py](model_training_continual.py)

This script is used to train the model. Run it with the following command:

```py
python model_training_continual.py
```

#### 4. [dataset_handler.py](dataset_handler.py)

This script is used to handle the dataset. Run it with the following command:

```py
python dataset_handler.py
```

#### 5. [rolling_prediction.py](rolling_prediction.py)

This script is used to make predictions. Run it with the following command:

```py
python rolling_prediction.py
```

#### 6. [stock_mock_API.py](stock_mock_API.py)

This script is used to mock the stock API. Run it with the following command:

```py
python stock_mock_API.py
```

## Results

The resuls can be seen in [stream_learning_demo.PNG](stream_learning_demo.PNG) and 
[stream_learning_essai_1.PNG](stream_learning_essai_1.PNG).

## References

- [1] Twitter et la bourse:  Résumé des articles cités: une corrélation possible, une causalité improbable
- [2] Yamina Tadjeddin, 2013, « La finance comportementale, une critique cognitive du paradigme classique de la 
finance » Idées économiques et sociales 2013/4 (N° 174), pages 16 et suivantes
- [3] [https://www.cairn.info/revue-idees-economiques-et-sociales-2013-4-page-16.htm](https://www.cairn.info/revue-idees-economiques-et-sociales-2013-4-page-16.htm)
- [4] Malcolm Baker & Jeffrey Wurgler, 2007. "Investor Sentiment in the Stock Market," NBER Working Papers, National 
Bureau of Economic Research, Inc.
- [5] Jean-Christophe Feraudet, 2020. « Analyse de Twitter en temps réel avec Kafka, Spark et mongoDB », 
[https://cedric.cnam.fr/vertigo/Cours/RCP216/docs/UASB03_Projet_Feraudet_v1.0.pdf](https://cedric.cnam.fr/vertigo/Cours/RCP216/docs/UASB03_Projet_Feraudet_v1.0.pdf)
, le CNAM
- [6] Singh, T., Kalra, R., Mishra, S. et al. An efficient real-time stock prediction exploiting incremental learning 
and deep learning. Evolving Systems (2022), [https://doi.org/10.1007/s12530-022-09481-x](https://doi.org/10.1007/s12530-022-09481-x)