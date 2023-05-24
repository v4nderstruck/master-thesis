# Thesis Proposal 

## Preliminaries

**Vertical Federated Learning**

Vertical Federated Learning (*VFL*) is a machine learning paradigm where
multiple parties collaborate to build a machine learning model without sharing
their private data [Zhang et. al. 2021][ref_survey_vfl]. In *VFL*, each party holds
data in a separate feature space which may intersect in the sample space. For
example, in a medical setting, some institution may store basic reports (e.g.
physiological data) of a patient while a medical sepecialist holds more
advanced diagnostic data (e.g. lab results, radiographs etc.). In this case,
the two institutions can collaborate to build a machine learning model given
that they have different data for the same patients. However, by doing so, each
party may reveal sensitive information about their private data. 
For example, by sharing intermediate results during the model training phase, a
party may accidentally enable other parties to recover the original data that
corresponds to the intermediate results (feature inference). Meanwhile, a party
that holds sensitive labels to a model training task may unknowingly leak them
while providing feedback for the optimization phase (label inference).  

**General Vertical Federated Model Training**

A prior to the model training phase, the parties have to exchange information to
find intersecting samples (i.e. patients). We will refer to parties as **active
participant** if they hold labels and **passive participant** if they
only have access to data. To find intersecting samples, participants may follow
a **private set intersection protocol** [Pinkas et. al 2014][ref_psi]. The protocol
can be applied pairwise for each active-passive participant to agree on common
training batches. From a privacy perspective, a participant of this protocol
will learn the intersecting identities without gaining additional knowledge
about other possible set memberships. This may already breach privacy
constraints for small and sensitive datasets (e.g. rare diseases). Nevertheless,
set intersections are necessary to match labels to data samples for 
state-of-the-art supervised machine learning. 

During model training, passive participants train separate local models on 
private data [Yang et. al. 2019][ref_survey_vfl_acm]. Each participant then
contributes intermediate results of their models to the active participant. 
which is responsible to provide feedback for the optimization phase of passive
participants. This general approach can be implemented in various ways. We will
discuss neural network based approaches in the following [Yin et. al. 2021][ref_yin_acm], 
[Yang et.al. 2023 (preprint)][ref_preprint_vfl_acm]:

- **Split Neural Network (SplitNN)**: Each passive participant performs the forwardpass
for the bottom part of a neural network.  The active participant collects
intermediate embeddings and performs the forwardpass for the top part of the
network. The active participant then updates the top part during backpropagation
and distributes gradients to the passive participants which are used for
respective local model optimization.
- **Aggregation**: Each passive participant performs the forwardpass for the
its local model and sends the prediction (model result) to the active
participant. The active participant calculates the error (and gradient) and sends
them to the passive participants. The passive participants then update their
local models based on the received gradient.

**Privacy Preserving Techniques**

Sharing intermediate embeddings and gradients during the model training phase, 
results in a privacy risk for all participants (reference: Gradient Inversion,
Model Inversion, Label Inversion attacks). To mitigate the risk, various 
techniques have been proposed. We will discuss the following techniques 
[Yin et. al. 2021][ref_yin_acm]:

- **Differential Privacy**: In a differential private defense strategy,
additional noise is added to the intermediate embeddings and gradients. While
this technique provides good privacy guarantees, it may also result in a
significant loss of model accuracy e.g. due to non converging gradient descent or
additive noise over mutliple epochs of training **(privacy-utility tradeoff)**.
- **Cryptography**: In a cryptography based defense strategy,
intermediate embeddings and gradients are encrypted before they are shared. 
This is typically done by using a multiparty computation protocol or homomorphic 
encryption scheme. Thus, the active participant may perform necessary operations 
without learning the intermediate embeddings and gradients. While this approach
is shown to achieve high model accuracy, it may result in a significant
computational overhead **(privacy-efficiency tradeoff)**.
- **Trusted (Third) Party**: In a trusted (third) party defense strategy, a 
party is responsible to collect intermediate embeddings and gradients from the
participants and perform the necessary operations. The third party may be
cryptographically secured (e.g. TEE). While this approach is shown to achieve
high model accuracy and low computational overhead, it requires a trusted party
**(privacy-trust tradeoff)**.
- **Other**: Other defense strategy include exchanging and modifying
intermediate embeddings and gradients to trick an adversary. Commonly, these
techniques are based on masking sensitive information and providing randomized
information. However, similar to differential privacy, these techniques may
result in a loss of model accuracy **(privacy-utility tradeoff)**.


**Transformers**

Recently, transformers have proven to be a powerful architecture for machine
learning in various domains. The initial paper proposes a multi-modal 
transformer architecture for medical data (imaging and non-imaging). The
architecture consumes input vectors of different modalities with positional
encoding (that's what transformers do) and feed them into a transformer encoder
where the attention mechanism is applied. The proposed architecture does not use
a transformer decoder. Instead, the encoder output is fed into a multi-layer
perceptron (MLP) for the prediction task. 


## The Thesis

**Goal**

In this Master thesis, we aim to implement a privacy preserving vertical
federated learning protocol for the medical transformer architecture proposed by
(referenced initial paper). We will explore privacy risks during training and
propose mitigation techniques.

**Research Questions**

We may explore the following research questions:

- How can multi-modal transformers be trained in a vertical federated setting?
  - The initial paper derives good model performance from joint training of
    multiple modalities (radiographs and other clinical data). 
  - In a vertical context, we may have to split the model for each
    modality/feature space (SplitNN) or implement some aggregation layer (Aggregation).
  - Challenges: loss of accuracy, how to make the attention mechanism work federatedly
  - Note: Machine learning heavy task
- Are transformers even a bigger privacy risk than "conventional" (MLP, CNN) Networks?
  - The proposed transformer only encodes based on attention, encoding very much
  mimics the original data
  - This may be reversible! Thus splitting the model "right where the encoder
  ends" is not privacy preserving at all which however is the way to do it for
  "conventional" networks!
  - Does it even open attacks across modalities due to positional encoding (e.g.
  radiographs to clinical data)?
  - Challenges: Model Inversion, Gradient Inversion attack on transformers
  - Note: Machine Learning heavy
- Apply cryptographic protocols efficiently to model training
  - We could use HE/MPC to protect intermediate results and gradients
  - Challenges: efficiency tradeoff 
  - Note: Cryptography protocol design
- Apply DP and other strategies to model training
  - Similar to above, but different techniques
  - Should consider transformer specific techniques
  - Challenges: accuracy tradeoff
- measure the tradeoff in privacy, utility and efficiency
- Combining DP and cryptographic protocols for hybrid model training?
  - develop some automatic parameter selection system for trading off utility,
  privacy and efficiency
  - requires measurement

**Possible Thesis Contributions**

A lot of papers in that area are generally structured as follows:
- they propose a model architecture and add privacy preserving techniques to it
- they show that privacy is preserved by showing that attacks are less
successful compared to no actions

Hence, we may also structure the thesis in a similar fashion. Note: it is probably too much
- we propose a multi modal transformer architecture in a federated setting
  - based on SplitNN architecture, the initial paper mimics that architecture already,
  although not in a federated setting. SplitNn will probably make federation
  simplier in terms of pure ML implementation work
  - This will result in a joint model for participants
  - Goal: comapareable model utility to the non-federated model
  - Note: would need Dataset access to train it
- we analyze the SplitNN architecture for privacy "risk"
  - in SplitNN setting, intermediate results and gradients are exchanged 
  - we should consider the honest-but-curious adversary model (most common in
  literature) without further protection techniques
  - Hence, how much privacy does the Transformer architecture leak?
  - Goal: show that data reconstruction and label inference is possible
- we consider privacy distances / metrics for model training and evaluate for the SplitNN 
  - in statistics, there are distances / metrics to express similarity of two
  data distributions e.g. Kullback-Leibler divergence and more
  - from these distances / metrics, we may derive optimality constraints (in
  trade-offs for example) for privacy preserving techniques
  - Goal: find meaningful privacy metrics
- we incrementally optimize on the privacy-utility-efficiency trade off for
model training based on given privacy metrics
  - from the results above, we start by introducing architecture specific
  counter measures to improve privacy (transformer specific). We will
  experimentally escalate the counter measures to more sophisticated techniques 
  in efficiency and utility dimensions to find optimal or at least good
  trade-offs 
  - Goal: show that privacy metrics can be used to optimize
  privacy-utiliy-efficiency trade-off 





[ref_survey_vfl]: https://www.sciencedirect.com/science/article/pii/S0950705121000381
[ref_psi]: https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-pinkas.pdf
[ref_survey_vfl_acm]: https://dl.acm.org/doi/pdf/10.1145/3298981
[ref_preprint_vfl_acm]: https://arxiv.org/pdf/2304.01829.pdf
[ref_yin_acm]: https://dl.acm.org/doi/pdf/10.1145/3460427
[ref_vit_leak]: https://openaccess.thecvf.com/content/CVPR2022/papers/Hatamizadeh_GradViT_Gradient_Inversion_of_Vision_Transformers_CVPR_2022_paper.pdf