# 01 — Literature map

[← back to README](README.md)

**152 distinct works** in six clusters (21 [READ-FIRST], 66 [RECOMMENDED], 65 [REFERENCE]). BibTeX keys match [`references.bib`](references.bib).

> **How these were checked (read this before citing anything).** This sandbox's network allows package registries but **blocks arxiv.org, Semantic Scholar, OpenReview, ACL Anthology, Hugging Face and most publisher sites**. So no paper PDF or abstract page could be opened directly. Each entry was checked by web search: the result listing had to show the canonical page (arXiv / proceedings / journal URL) with matching title and authors. Most were confirmed by two or more listings. "Checked against" names the listing(s) used. Consequences:
> * Summaries are based on **abstracts as shown in search results**. A few entries say they used more (e.g. the Operadic Consistency entry, whose code repository on GitHub *was* readable). No intro/method sections were read, despite the original plan.
> * Numbers quoted in summaries (AUROCs, correlations, percentages) come from abstracts or search snippets. **Check them against the PDF before citing.**
> * Author lists marked "et al.", "(not re-verified)" or "unverified" are incomplete. Venues marked "per …" are second-hand.
> * Anything that could not be confirmed at all was dropped and listed in [CHANGELOG_or_NOTES.md](CHANGELOG_or_NOTES.md#could-not-verify).
>
> Tags: **[READ-FIRST]** = read before doing anything else in this direction · **[RECOMMENDED]** = read when you work on that avenue · **[REFERENCE]** = cite/consult as needed.

## Contents

- [Cluster A: Categorical deep learning, categorical probability & information](#cluster-a-categorical-deep-learning-categorical-probability--information) (22)
- [Cluster B: Compositional semantics and category theory × LLMs (incl. the closest prior art to Will's test)](#cluster-b-compositional-semantics-and-category-theory--llms-incl-the-closest-prior-art-to-wills-test) (18)
- [Cluster C: Sheaves, cohomology, contextuality & consistency](#cluster-c-sheaves-cohomology-contextuality--consistency) (21)
- [Cluster D: Causal abstraction, mechanistic interpretability & representation structure](#cluster-d-causal-abstraction-mechanistic-interpretability--representation-structure) (28)
- [Cluster E: Open games, categorical cybernetics, agent foundations & formal safety](#cluster-e-open-games-categorical-cybernetics-agent-foundations--formal-safety) (31)
- [Cluster F: Empirical LLM compositionality, consistency & uncertainty (the baselines)](#cluster-f-empirical-llm-compositionality-consistency--uncertainty-the-baselines) (32)


## Cluster A: Categorical deep learning, categorical probability & information

### [READ-FIRST] `gavranovic2024categorical`
Bruno Gavranović, Paul Lessard, Andrew Dudzik, Tamara von Glehn, João G. M. Araújo, Petar Veličković, 2024. *Position: Categorical Deep Learning is an Algebraic Theory of All Architectures*. ICML 2024, PMLR 235:15209–15241. (The v1 title was "Categorical Deep Learning: An Algebraic Theory of Architectures".)  
URL: <https://arxiv.org/abs/2402.15332>  
Topic: CT for architectures · Depth read: abstract (DEEP-READ TODO)  
Checked against: WebSearch results listing https://arxiv.org/abs/2402.15332v2 and https://proceedings.mlr.press/v235/gavranovic24a.html

- **Summary.** The paper proposes monads and their algebras, valued in a 2-category of parametric maps, as one language for both the constraints on an architecture and its implementation. Monads induced by group actions recover Geometric Deep Learning. Recurrent and recursive models appear as lax algebras for free parametric monads, and weight tying is modelled explicitly.
- **Why it matters for us.** This is the main "architecture = algebra" reference. It gives a precise sense in which a model is supposed to *respect* structure, such as an equivariance or an algebra law. delta_comp is a test of exactly this kind of structure-preservation, applied to behaviour instead of weights. The link is conceptual: the paper does not cover LLM outputs or hallucination.

### [READ-FIRST] `fritz2020synthetic`
Tobias Fritz, 2020. *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics*. Advances in Mathematics 370, 107239.  
URL: <https://arxiv.org/abs/1908.07021>  
Topic: Markov categories · Depth read: abstract (DEEP-READ TODO)  
Checked against: WebSearch result listing https://arxiv.org/abs/1908.07021v8 and https://arxiv.org/abs/1908.07021v6

- **Summary.** The paper develops Markov categories, symmetric monoidal categories with copy and discard, as a synthetic framework for probability and statistics. It covers conditioning, conditional independence, almost-sure equality and sufficient statistics. It proves abstract versions of the semigraphoid properties and of the Fisher–Neyman, Basu and Bahadur theorems.
- **Why it matters for us.** This is the right ambient category for our functoriality test. An LLM answering a hop is a Markov kernel, so "direct vs stepwise" compares a kernel with a Kleisli composite of kernels. delta_comp is then a defect of composition in a Markov category, and determinism and almost-sure equality give clean definitions of "no hallucination".

### [READ-FIRST] `perrone2024markov`
Paolo Perrone, 2024. *Markov Categories and Entropy*. IEEE Transactions on Information Theory 70(3). arXiv 2022.  
URL: <https://arxiv.org/abs/2212.11719>  
Topic: Markov categories / entropy · Depth read: abstract (DEEP-READ TODO)  
Checked against: WebSearch result listing https://arxiv.org/abs/2212.11719v2 and https://act2023.github.io/papers/paper12.pdf

- **Summary.** The paper defines entropy in any Markov category with a chosen divergence as "how far a source or channel is from being deterministic". This is measured as the divergence between copying the output and taking two independent samples. Mutual information is defined similarly, and with KL divergence the construction recovers Shannon entropy.
- **Why it matters for us.** This is a ready-made bridge between our two signals. "Distance from determinism" is exactly the self-consistency or semantic-entropy style hallucination signal, and delta_comp is "distance from functoriality" in the same Markov category. The paper suggests a unified divergence-parametrised family of signals.

### [RECOMMENDED] `fong2019backprop`
Brendan Fong, David I. Spivak, Rémy Tuyéras, 2019. *Backprop as Functor: A compositional perspective on supervised learning*. LICS 2019 (34th ACM/IEEE Symposium on Logic in Computer Science). arXiv 2017.  
URL: <https://arxiv.org/abs/1711.10455>  
Topic: Lenses / learners · Depth read: abstract  
Checked against: WebSearch results listing https://arxiv.org/abs/1711.10455v3 and https://dspace.mit.edu/bitstream/1721.1/123513/1/learners.pdf

- **Summary.** The paper defines a symmetric monoidal category Learn whose morphisms are learners with a "request" function that sends information backwards. It shows that gradient descent with a fixed step size and a suitable error function is a monoidal functor Para → Learn. It also relates Learn to lenses and open games.
- **Why it matters for us.** This is the founding "is the learning procedure itself a functor?" result. Functoriality here means that composing then training equals training then composing. That is the training-time analogue of our inference-time check F(g∘f) = F(g)∘F(f). It gives a good framing line for the paper.

### [RECOMMENDED] `cruttwell2022categorical`
G. S. H. Cruttwell, Bruno Gavranović, Neil Ghani, Paul Wilson, Fabio Zanasi, 2022. *Categorical Foundations of Gradient-Based Learning*. ESOP 2022 (Programming Languages and Systems, LNCS), DOI 10.1007/978-3-030-99336-8_1 (venue name inferred from the DOI; unconfirmed). arXiv 2021.  
URL: <https://arxiv.org/abs/2103.01931>  
Topic: Para / lenses / optics · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2103.01931 and https://discovery.ucl.ac.uk/id/eprint/10160499/2/Zanasi_978-3-030-99336-8_1.pdf

- **Summary.** The paper gives a semantics for gradient-based learning built from three pieces: lenses, parametric maps (Para), and reverse derivative categories. Losses, optimisers and learning rates become composable components. The framework also covers discrete settings such as Boolean circuits, and the authors built a Python implementation.
- **Why it matters for us.** It is the standard reference for the Para + Lens toolkit. Use it if we want to describe a "verifier-in-the-loop" pipeline in which verification feedback flows backwards through a reasoning DAG. The link to hallucination itself is thin.

### [RECOMMENDED] `shiebler2021category`
Dan Shiebler, Bruno Gavranović, Paul Wilson, 2021. *Category Theory in Machine Learning*. arXiv preprint (also presented at ACT 2021).  
URL: <https://arxiv.org/abs/2106.07032>  
Topic: Survey · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2106.07032

- **Summary.** A survey of the motivations, goals and common themes of applied CT in ML. It covers three areas: gradient-based learning, probability, and equivariant learning.
- **Why it matters for us.** This is the best single entry point for the survey's related-work section. It covers both halves of this cluster, deep-learning structure and Markov-category probability.

### [RECOMMENDED] `maruyama2025categorical`
Yoshihiro Maruyama, 2025. *Categorical Equivariant Deep Learning: Category-Equivariant Neural Networks and Universal Approximation Theorems*. arXiv preprint.  
URL: <https://arxiv.org/abs/2511.18417>  
Topic: Equivariance / geometric DL (2025) · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2511.18417v2 and https://arxiv.org/html/2511.18417v1

- **Summary.** The paper defines category-equivariant neural networks (CENNs). These unify group/groupoid-, poset/lattice-, graph- and sheaf-equivariant networks by treating equivariance as naturality in a topological category with Radon measures. Its main result is that finite-depth CENNs are dense in the space of continuous equivariant transformations.
- **Why it matters for us.** This is the clearest recent statement that "equivariance = naturality". Our consistency checks are naturality squares on model behaviour, and this paper suggests treating violations as a measurable distance from the equivariant subspace.

### [RECOMMENDED] `dudzik2022graph`
Andrew Dudzik, Petar Veličković, 2022. *Graph Neural Networks are Dynamic Programmers*. NeurIPS 2022.  
URL: <https://arxiv.org/abs/2203.15544>  
Topic: Algorithmic alignment / DP · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2203.15544 and https://neurips.cc/virtual/2022/poster/53143

- **Summary.** The paper uses category theory and abstract algebra (polynomial functors, pullback/pushforward, monads) to show a structural correspondence between GNN message passing and dynamic programming. This goes beyond earlier case-by-case observations such as Bellman-Ford.
- **Why it matters for us.** Our budgeted-verification oracle is a DP over a claim DAG. This paper is the categorical bridge to learning a DP-aligned approximation to that oracle with a GNN. A concrete follow-up: train a GNN on DAG + p_false to imitate the DP oracle.

### [RECOMMENDED] `baez2011characterization`
John C. Baez, Tobias Fritz, Tom Leinster, 2011. *A Characterization of Entropy in Terms of Information Loss*. Entropy 13(11):1945–1957. DOI 10.3390/e13111945.  
URL: <https://arxiv.org/abs/1106.1791>  
Topic: Categorical information theory · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/1106.1791v3 and https://doaj.org/article/4537eddd4faf495082eb23c93c15c38e

- **Summary.** The paper studies information loss, the entropy change along a measure-preserving map, instead of the entropy of a single distribution. Shannon entropy is shown to be the unique measure of information loss that is functorial, convex-linear and continuous, and the result extends to Tsallis entropy.
- **Why it matters for us.** "Information loss is a functor" is a direct template for asking whether a hallucination score should be functorial along a reasoning chain. Their axioms (functoriality, convex-linearity, continuity) can serve as desiderata for any compositional hallucination metric. One example is whether delta_comp is subadditive along chains.

### [RECOMMENDED] `baez2014bayesian`
John C. Baez, Tobias Fritz, 2014. *A Bayesian characterization of relative entropy*. Theory and Applications of Categories 29(16):422–456 (page range differs across indexes: 421 or 422 to 456).  
URL: <https://arxiv.org/abs/1402.3067>  
Topic: Categorical information theory · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/1402.3067v1 and https://www.maths.tcd.ie/EMIS/journals/TAC/volumes/29/16/29-16abs.html

- **Summary.** The paper characterises KL divergence via the category FinStat of finite sets with measure-preserving maps and "hypotheses" s. Any convex-linear, lower-semicontinuous functor FinStat → [0,∞] that vanishes when s is optimal is a scalar multiple of relative entropy.
- **Why it matters for us.** It shows that relative entropy measures how far a hypothesis (inference) is from optimal, functorially. That is a principled alternative to TV for delta_comp (KL from stepwise to direct), and it comes with a compositional justification.

### [RECOMMENDED] `smithe2020bayesian`
Toby St. Clere Smithe, 2020. *Bayesian Updates Compose Optically*. arXiv preprint.  
URL: <https://arxiv.org/abs/2006.01631>  
Topic: Bayesian lenses · Depth read: abstract (DEEP-READ TODO)  
Checked against: WebSearch result listing https://arxiv.org/abs/2006.01631

- **Summary.** The paper proves that the Bayesian inversion of a composite channel equals the lens composite of the inversions of its parts ("Bayesian lenses compose optically", Theorem 5.2). It gives both abstract and concrete proofs, for discrete and continuous states.
- **Why it matters for us.** This is the inverse-direction analogue of our test. For exact Bayesians, backward inference over x→y→z composes. An LLM asked "which x led to z?" directly vs stepwise gives a backward-direction delta_comp. This is a second, independent consistency check with a theorem saying it should be zero.

### [RECOMMENDED] `braithwaite2023compositional`
Dylan Braithwaite, Jules Hedges, Toby St Clere Smithe, 2023. *The Compositional Structure of Bayesian Inference*. MFCS 2023, LIPIcs 272, 24:1–24:15. DOI 10.4230/LIPIcs.MFCS.2023.24.  
URL: <https://arxiv.org/abs/2305.06112>  
Topic: Bayesian lenses · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2305.06112v1 and https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2023.24

- **Summary.** The paper shows how Bayesian inversion of a compositional process can be computed piecewise. Inversion is framed as a state-dependent morphism in a fibred category over Markov kernels and linked to the lens pattern. It is the published consolidation of arXiv:2006.01631 and arXiv:2209.14728.
- **Why it matters for us.** Cite this peer-reviewed version for "Bayesian inversion is compositional". It supports a backward/abductive version of the functoriality probe.

### [RECOMMENDED] `yin2022markov`
Yimu Yin, Jiji Zhang, 2022. *Markov categories, causal theories, and the do-calculus*. arXiv preprint (a version listed in Studies in Logic 14(6); unconfirmed).  
URL: <https://arxiv.org/abs/2204.04821>  
Topic: Causal DAGs in Markov categories · Depth read: abstract (DEEP-READ TODO)  
Checked against: WebSearch result listing https://arxiv.org/pdf/2204.04821

- **Summary.** The paper canonically associates a free Markov category with a DAG and uses it to study causal independence/separation, causal conditionals and the decomposition of intervention effects. It derives a syntactic do-calculus, claimed to be as strong as Pearl's for causal Bayesian networks.
- **Why it matters for us.** This is the most direct categorical home for the parent project's claim DAG. Each claim is a node and the reasoning DAG generates a free Markov category, so "verifying a claim" becomes an intervention (do(claim = true)). Expected damage via descendant counts could be refined to interventional effect on the conclusion.

### [RECOMMENDED] `fritz2023dseparation`
Tobias Fritz, Andreas Klingler, 2023. *The d-Separation Criterion in Categorical Probability*. Journal of Machine Learning Research 24(46):1–49.  
URL: <https://arxiv.org/abs/2207.05740>  
Topic: Causal DAGs in Markov categories · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2207.05740v3 and https://jmlr.org/papers/v24/22-0916.html

- **Summary.** The paper introduces a categorical framework for causal models and a categorical d-separation, and proves an abstract d-separation criterion. The result covers standard Borel probability and also deterministic and possibilistic networks.
- **Why it matters for us.** d-separation tells you which claims cannot influence the conclusion given verified claims. That suggests a principled refinement of "descendant count" in the damage model: count only descendants not d-separated from the final answer by already-verified nodes.

### [REFERENCE] `gavranovic2024fundamental`
Bruno Gavranović, 2024. *Fundamental Components of Deep Learning: A category-theoretic approach*. PhD thesis, University of Strathclyde. arXiv preprint.  
URL: <https://arxiv.org/abs/2403.13001>  
Topic: Para / optics (thesis) · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2403.13001 and https://pureportal.strath.ac.uk/en/studentTheses/fundamental-components-of-deep-learning-a-category-theoretic-appr/

- **Summary.** Part I develops parameterisation and bidirectionality, which combine into "parametric weighted optics" as a categorical model of neural networks. Part II applies this to backpropagation, architectures and supervised learning.
- **Why it matters for us.** This is the most complete pedagogical treatment of Para and optics. It is a reference for notation, not a direct safety contribution.

### [REFERENCE] `crescenzi2024towards`
Francesco Riccardo Crescenzi, 2024. *Towards a Categorical Foundation of Deep Learning: A Survey*. arXiv preprint (a Bologna thesis supervised by Fabio Zanasi; this attribution comes from secondary sources).  
URL: <https://arxiv.org/abs/2410.05353>  
Topic: Survey · Depth read: abstract  
Checked against: WebSearch results listing https://arxiv.org/pdf/2410.05353 and https://arxiv.org/html/2410.05353v2

- **Summary.** An updated survey of CT applied to deep learning. It is organised around four constructs, including parametric optics for gradient-based learning.
- **Why it matters for us.** A more recent survey than shiebler2021category, useful for checking coverage. It has no safety content.

### [REFERENCE] `fritz2021definetti`
Tobias Fritz, Tomáš Gonda, Paolo Perrone, 2021. *De Finetti's Theorem in Categorical Probability*. Journal of Stochastic Analysis 2(4), Article 6.  
URL: <https://arxiv.org/abs/2105.02639>  
Topic: Markov categories / exchangeability · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2105.02639

- **Summary.** The paper gives a new proof of de Finetti's theorem for permutation-invariant probability measures, stated in the language of Markov categories. It derives versions of the theorem in several Markov categories and recovers the measure-theoretic theorem for standard Borel spaces.
- **Why it matters for us.** The link is thin but real. Repeated LLM samples are exchangeable, so de Finetti justifies modelling them as i.i.d. given a latent "belief". That is the latent our sampled answer distributions estimate.

### [REFERENCE] `braithwaite2022dependent`
Dylan Braithwaite, Jules Hedges, 2022. *Dependent Bayesian Lenses: Categories of Bidirectional Markov Kernels with Canonical Bayesian Inversion*. arXiv preprint.  
URL: <https://arxiv.org/abs/2209.14728>  
Topic: Bayesian lenses · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/2209.14728?context=cs

- **Summary.** The paper generalises Bayesian lenses so that the backward object depends on states of the forward object. This gives a more canonical Bayesian inversion in Markov categories.
- **Why it matters for us.** A technical reference only. Its material is superseded by braithwaite2023compositional.

### [REFERENCE] `cho2019disintegration`
Kenta Cho, Bart Jacobs, 2019. *Disintegration and Bayesian Inversion via String Diagrams*. Mathematical Structures in Computer Science 29:938–971. arXiv 2017.  
URL: <https://arxiv.org/abs/1709.00322>  
Topic: String diagrams / Bayesian inversion · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/1709.00322v3 and https://www.cs.ru.nl/K.Cho/papers/disintegration.pdf

- **Summary.** The paper gives a string-diagrammatic (affine CD-category) account of disintegration and Bayesian inversion, which turn a joint state or a channel into a channel in the opposite direction. It treats discrete and measure-theoretic probability, and works through naive Bayes classification with the EfProb tool.
- **Why it matters for us.** It provides the graphical calculus for drawing our direct-vs-stepwise test as a string-diagram equation and for defining when two channels are equal almost surely. That is useful for the paper's figures.

### [REFERENCE] `fong2013causal`
Brendan Fong, 2013. *Causal Theories: A Categorical Perspective on Bayesian Networks*. MSc thesis, University of Oxford. arXiv preprint.  
URL: <https://arxiv.org/abs/1301.6201>  
Topic: Causal DAGs in Markov categories · Depth read: abstract  
Checked against: WebSearch result listing https://web3.arxiv.org/abs/1301.6201 and https://arxiv.org/pdf/1301.6201

- **Summary.** The thesis develops "causal theories", a formal graphical framework for causal reasoning in which a factorisation is chosen explicitly rather than merely required to exist. Models in measurable spaces with stochastic maps slightly generalise Bayesian networks.
- **Why it matters for us.** The historical root of the DAG-as-category view used by yin2022markov and fritz2023dseparation. Cite for lineage.

### [REFERENCE] `fong2019lenses`
Brendan Fong, Michael Johnson, 2019. *Lenses and Learners*. Bx@PLW 2019, CEUR Workshop Proceedings vol. 2355, pp. 16–29.  
URL: <https://arxiv.org/abs/1903.03671>  
Topic: Lenses / learners · Depth read: abstract  
Checked against: WebSearch result listing https://arxiv.org/abs/1903.03671v1 and https://researchr.org/publication/FongJ19/bibtex

- **Summary.** The paper gives a faithful, identity-on-objects, symmetric monoidal functor from the category of learners to a category of symmetric lenses. This connects supervised learning to bidirectional transformations.
- **Why it matters for us.** A background reference for the lens view. Thin link to safety.

### [REFERENCE] `kamiya2021category`
Kotaro Kamiya, John Welliaveetil, 2021. *A category theory framework for Bayesian learning*. arXiv preprint.  
URL: <https://arxiv.org/abs/2111.14293>  
Topic: Categorical Bayesian learning --- · Depth read: abstract (from the search summary: uses Markov categories and Bayesian inversion to formalise Bayesian learning)  
Checked against: WebSearch result listing https://arxiv.org/abs/2111.14293

- **Summary.** A categorical framework for Bayesian learning built on Markov categories and Bayesian inversion, in the spirit of the learner/lens frameworks.
- **Why it matters for us.** Possibly relevant for calibration and uncertainty updating. I could confirm little beyond the title and authors, so treat it as a lead.


## Cluster B: Compositional semantics and category theory × LLMs (incl. the closest prior art to Will's test)

### [READ-FIRST] `bottman2026operadic`
Nathaniel Bottman, Yinhong Liu, Kyle Richardson, 2026. *Operadic consistency: a label-free signal for compositional reasoning failures in LLMs*. NeurIPS 2026 (per the authors' repo README); arXiv:2606.13649.  
URL: <https://arxiv.org/abs/2606.13649>  
Topic: CT x LLM hallucination / compositional consistency · Depth read: abstract + companion code (README and `experiments/nonthinking_oc/run_together.py` read)  
Checked against: WebSearch listing of https://arxiv.org/abs/2606.13649 and https://arxiv.org/html/2606.13649v1; WebFetch of https://github.com/natebottman/operadic-consistency-paper (title, authors, NeurIPS 2026 and bibtex in README)

- **Summary.** Defines operadic consistency as the requirement that a model's *direct* answer to a multi-hop question agrees with the answer it reaches by *decomposition*: answer step-1, substitute that answer into the step-2 template, then answer step-2. The scalar version, OC, is computed in code as token-F1(direct, decomposed) between two greedy (T=0) answers, thresholded at 0.5. Across 12 instruction-tuned LLMs (4B-671B) on HotpotQA, **MuSiQue**, StrategyQA and DROP, OC correlates with accuracy at Pearson r of about 0.86-0.94. It adds information beyond CoT self-consistency and semantic entropy, and it improves selective prediction (AUARC/AUROC). It is also run on 5 "thinking" models, and its baselines include P(True), decomposed-SC, NLI and two PRMs.
- **Why it matters for us.** **This is the main novelty risk.** It is essentially Will's test, F(g∘f)(x) vs F(g)(F(f)(x)) on MuSiQue as a label-free hallucination signal, framed with operads and published at NeurIPS 2026. Will's remaining room: (a) comparing full *answer distributions* with TV distance instead of one greedy pair compared by token-F1; (b) chains longer than depth 2 and partial collapses (the theory paper mentions these, but the code only does depth 2); (c) using the signal to pick which claims to verify under a budget (the parent DAG project). Will must cite this paper and position his work against it.

### [READ-FIRST] `bottman2026operads`
Nathaniel Bottman, Kyle Richardson, 2026. *Operads for compositional reasoning in LLMs*. arXiv preprint arXiv:2606.13634 (ICML 2026 virtual listings exist at icml.cc/virtual/2026/68317 and /69344; I could not confirm whether these are workshop or main track).  
URL: <https://arxiv.org/abs/2606.13634>  
Topic: CT x LLM hallucination / theory · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/2606.13634 and the companion repo README (WebFetch https://github.com/natebottman/operadic-consistency-paper)

- **Summary.** Gives question decomposition a formal footing through a "questions operad": operations are question templates, composition substitutes sub-answers into templates, and QA models are interpreted as *algebras* over that operad. It defines "reasoning robustness", meaning consistency across partial collapses of a decomposition tree, and its scalar form, operadic consistency. The paper reports that this scalar correlates with accuracy, while temperature-based self-consistency does not.
- **Why it matters for us.** This is the theory companion to the paper above. "QA model as an operad algebra" is the operadic version of Will's "LLM as a functor". Partial collapses of a tree are close to his DAG of claims. He should read it before writing his formal section, to avoid re-deriving it and to choose a framing that differs (functor/category vs operad, distributional vs pointwise).

### [READ-FIRST] `chen2024twofailures`
Angelica Chen, Jason Phang, Alicia Parrish, Vishakh Padmakumar, Chen Zhao, Samuel R. Bowman, Kyunghyun Cho, 2024. *Two Failures of Self-Consistency in the Multi-Step Reasoning of LLMs*. Transactions on Machine Learning Research (TMLR); arXiv:2305.14279.  
URL: <https://arxiv.org/abs/2305.14279>  
Topic: consistency / multi-hop (non-CT, cited by Will) · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2305.14279v4 and https://par.nsf.gov/biblio/10542787-two-failures-self-consistency-multi-step-reasoning-llms

- **Summary.** Defines two kinds of self-consistency for multi-step reasoning. *Hypothetical consistency* asks whether a model can predict its own output in a hypothetical other context. *Compositional consistency* asks whether its final answer stays the same when an intermediate sub-step is replaced by the model's own earlier output for that sub-step. The authors argue that consistency is under-evaluated because benchmarks score only correctness, and that LLMs fail both kinds.
- **Why it matters for us.** Compositional consistency here is the non-categorical forerunner of the functoriality test, and it predates both Operadic Consistency and Will's work. Will must cite it as the empirical origin of the direct-vs-composed comparison.

### [RECOMMENDED] `liu2026intent`
Shuoling Liu, Zhiquan Tan, Kun Yi, Hui Wu, Yihan Li, Jiangpeng Yan, Liyuan Chen, Kai Chen, Qiang Yang, 2026. *From Intent to Evidence: A Categorical Approach for Structural Evaluation of Deep Research Agents*. arXiv:2603.25342 (a NeurIPS 2026 poster listing exists: neurips.cc/virtual/2026/poster/153875).  
URL: <https://arxiv.org/abs/2603.25342>  
Topic: CT x LLM agents / evaluation · Depth read: abstract (search summary of HTML excerpts)  
Checked against: WebSearch listing of https://arxiv.org/pdf/2603.25342 (authors also confirmed on the sotaverified and ScienceCast listings)

- **Summary.** Models a deep-research agent's search and reasoning as functors between categories of queries, web evidence and logic. It states a "Chain-of-Search Consistency" (functoriality) property: an ideal agent preserves composition across multi-hop retrieval, and it derives transitivity of deduction from the composition axiom. It includes a formal characterisation of hallucination (Remark 3.6, not read) and reports that current agents largely fail at multi-hop structural synthesis.
- **Why it matters for us.** This is a second 2026 paper that states "functoriality across multi-hop chains" explicitly, for *agents* rather than bare LLM answer distributions. It is a novelty risk for the framing (though not for the TV-distance metric) and should be cited.

### [RECOMMENDED] `bradley2022enriched`
Tai-Danae Bradley, John Terilla, Yiannis Vlassopoulos, 2021 (v2 Nov 2021). *An enriched category theory of language: from syntax to semantics*. arXiv preprint arXiv:2106.07890 (math.CT, cs.CL). Journal version not verified.  
URL: <https://arxiv.org/abs/2106.07890>  
Topic: compositional semantics / enriched CT · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2106.07890v2

- **Summary.** Builds a category enriched over [0,1] in which objects are texts and hom-objects are the conditional probability that one text extends another, as given by a language model's continuation probabilities. Through the enriched Yoneda embedding, a text's *meaning* is taken to be its representable [0,1]-valued copresheaf, the profile of all its possible continuations.
- **Why it matters for us.** This is the standard way to make "an LLM is a functor" precise. It is where the probabilities in Will's F(f)(x) can be given categorical status, and where TV distance between continuation distributions becomes a distance between copresheaves.

### [RECOMMENDED] `bradley2025magnitude`
Tai-Danae Bradley, Juan Pablo Vigneaux, 2025. *The magnitude of categories of texts enriched by language models*. Theory and Applications of Categories, 44(37); arXiv:2501.06662.  
URL: <https://arxiv.org/abs/2501.06662>  
Topic: compositional semantics / enriched CT · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/2501.06662 and https://tac.mta.ca/tac/volumes/44/37/44-37abs.html

- **Summary.** Uses an LM's next-token probabilities to [0,1]-enrich a category of texts in the Bradley-Terilla-Vlassopoulos style. It shows that the magnitude function is a sum over prompts of Tsallis t-entropies of next-token distributions, plus the cardinality of the possible outputs. A derivative of the magnitude recovers a sum of Shannon entropies. It also computes the zeroth and first magnitude homology.
- **Why it matters for us.** This links a categorical invariant (magnitude) to output-distribution entropy, which is the quantity behind entropy-based hallucination detectors. It could give an "entropy of a chain" a categorical reading. The link to detection is suggestive, not established.

### [RECOMMENDED] `gonzalez2023beyond`
Javier González, Aditya V. Nori, 2023. *Beyond Words: A Mathematical Framework for Interpreting Large Language Models*. arXiv preprint arXiv:2311.03033.  
URL: <https://arxiv.org/abs/2311.03033>  
Topic: CT x LLM / formal definitions · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/2311.03033

- **Summary.** Proposes "Hex", a mathematical framework that gives precise definitions of hallucination, alignment, self-verification and chain-of-thought reasoning. A main result separates chain-of-thought *reasoning* from chain-of-thought *prompting* and gives conditions under which they are equivalent.
- **Why it matters for us.** Will already cites it. It is the closest earlier attempt to *define* hallucination formally (and categorically) and to relate stepwise and direct computation. Useful for definitions in Will's background section.

### [RECOMMENDED] `yang2025metaqa`
Borui Yang, Md Afif Al Mamun, Jie M. Zhang, Gias Uddin, 2025. *Hallucination Detection in Large Language Models with Metamorphic Relations*. ESEC/FSE 2025; arXiv:2502.15844.  
URL: <https://arxiv.org/abs/2502.15844>  
Topic: hallucination detection / consistency (non-CT, cited by Will) · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2502.15844v2 and https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/48/Hallucination-Detection-in-Large-Language-Models-with-Metamorphic-Relations

- **Summary.** MetaQA is a zero-resource hallucination detector. It mutates responses into synonym and antonym variants and checks whether the expected logical relations (metamorphic relations) hold, treating a violation as a sign of hallucination. On TruthfulQA, HotpotQA and FreshQA across GPT-4, GPT-3.5, Llama3 and Mistral it beats SelfCheckGPT; for example, Mistral-7B F1 is 0.435 vs 0.205. (Note: the published title says "Large Language Models", not "LLMs".)
- **Why it matters for us.** Metamorphic relations are equations a correct model should satisfy, and functoriality is one such relation. It is a strong non-categorical baseline that Will should compare against or at least cite.

### [RECOMMENDED] `huntsman2024sheaves`
Steve Huntsman, Michael Robinson, Ludmilla Huntsman, 2024. *Prospects for inconsistency detection using large language models and sheaves*. arXiv:2401.16713.  
URL: <https://arxiv.org/abs/2401.16713>  
Topic: sheaves x LLM consistency · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2401.16713v1

- **Summary.** Shows that LLMs can numerically rate the logical consistency of small sets of claims. It proposes sheaf theory to glue these *local* ratings into a *global* consistency assessment over hypertexts such as laws and social media, and argues that sheaf tooling tolerates LLM output variability.
- **Why it matters for us.** The closest earlier work for the parent DAG project. Local LLM verdicts on claims combined into global consistency via sheaves is a natural categorical model for "which claims to verify". Sheaf cohomology could flag where verification is most informative.

### [REFERENCE] `bradley2024structure`
Tai-Danae Bradley, Juan Luis Gastaldi, John Terilla, 2024. *The structure of meaning in language: parallel narratives in linear algebra and category theory*. Notices of the American Mathematical Society 71(2):174-185. doi:10.1090/noti2868.  
URL: <https://www.ams.org/journals/notices/202402/rnoti-p174.pdf>  
Topic: compositional semantics / exposition · Depth read: abstract  
Checked against: WebSearch listing of that AMS PDF and https://pub.sandboxaq.com/publications/the-structure-of-meaning-in-language-parallel-narratives-in-linear-algebra-and-category-theory

- **Summary.** An expository piece that tells two parallel stories: word embeddings from linear algebra, and a category-theoretic version in which a category is replaced by its presheaf category. In the categorical version the output is a lattice of formal concepts rather than embeddings, coming from a simplified piece of enriched category theory.
- **Why it matters for us.** The most readable entry point to the Bradley programme for an undergraduate. It offers useful intuition but no direct hallucination content.

### [REFERENCE] `coecke2010discocat`
Bob Coecke, Mehrnoosh Sadrzadeh, Stephen Clark, 2010. *Mathematical Foundations for a Compositional Distributional Model of Meaning*. Linguistic Analysis 36 (Lambek Festschrift); arXiv:1003.4394.  
URL: <https://arxiv.org/abs/1003.4394>  
Topic: compositional semantics / DisCoCat · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/1003.4394 (also https://www.cs.ox.ac.uk/publications/publication4763-abstract.html)

- **Summary.** Combines vector-space word meanings with Lambek pregroup grammar inside a compact closed category. Grammatical reductions become morphisms, so a sentence's meaning is computed from its words' meanings: the "DisCoCat" model. The paper sets up the mathematics only, with no implementation.
- **Why it matters for us.** This is the founding example of "meaning should be functorial in syntax", the historical root of the functoriality intuition. Its relevance to LLM hallucination is conceptual only.

### [REFERENCE] `coecke2021discocirc`
Bob Coecke, 2021 (arXiv 2019). *The Mathematics of Text Structure*. Book chapter (Springer, pp. 181-217, per a citing paper; volume not verified); arXiv:1904.03478.  
URL: <https://arxiv.org/abs/1904.03478>  
Topic: compositional semantics / DisCoCirc · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/1904.03478v1

- **Summary.** Introduces DisCoCirc, which extends DisCoCat from sentences to whole texts. Word meanings become evolving states, sentences become processes that update them, and a text becomes a single string diagram (circuit).
- **Why it matters for us.** Its "text as a composed circuit of processes" picture is close to modelling a reasoning trace as a composite of morphisms, which fits the claim-DAG project. The relevance is conceptual.

### [REFERENCE] `wangmascianica2023distilling`
Vincent Wang-Mascianica, Jonathon Liu, Bob Coecke, 2023. *Distilling Text into Circuits*. arXiv:2301.10595. (Full first names were not visible in the listing beyond "Wang-Mascianica, Liu, and Coecke". The first names given here are my best knowledge and should be checked before citing.)  
URL: <https://arxiv.org/abs/2301.10595>  
Topic: compositional semantics / DisCoCirc · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2301.10595v1 (surfaced in the DisCoCirc search)

- **Summary.** Implements DisCoCirc for a fragment of English, converting text into circuits.
- **Why it matters for us.** Shows that the circuit view can be implemented. The link to safety is thin.

### [REFERENCE] `kartsaklis2021lambeq`
Dimitri Kartsaklis et al. (10 authors, Cambridge Quantum Computing), 2021. *lambeq: An Efficient High-Level Python Library for Quantum NLP*. arXiv:2110.04236.  
URL: <https://arxiv.org/abs/2110.04236>  
Topic: compositional semantics / tooling · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2110.04236v1 (full author list not shown in the listing)

- **Summary.** An open-source toolkit that turns sentences into string diagrams and then quantum circuits under a chosen compositional model. Version 1 has three models and builds on DisCoPy for string diagrams.
- **Why it matters for us.** Tooling only. DisCoPy, the backend, could be used to draw and check the commuting diagrams in Will's paper. Otherwise it is not relevant to hallucination.

### [REFERENCE] `chytas2024eccv`
Sotirios Panagiotis Chytas, Hyunwoo J. Kim, Vikas Singh, 2024. *Understanding Multi-compositional learning in Vision and Language models via Category Theory*. ECCV 2024 (LNCS; doi:10.1007/978-3-031-73195-2_19).  
URL: <https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06472.pdf>  
Topic: CT x representations · Depth read: abstract  
Checked against: WebSearch listing of https://eccv2024.ecva.net/virtual/2024/poster/451 and https://mlanthology.org/eccv/2024/chytas2024eccv-understanding

- **Summary.** Uses compositional zero-shot learning (attribute-object compositions) as a running example. It argues that the latent space should respect structure that follows from basic category-theory axioms, and gives a cross-attention solution for single- and multi-attribute compositions.
- **Why it matters for us.** An example of category-theory axioms used as *constraints that representations should satisfy*, which is the representation-level analogue of Will's output-level test. It is vision-language, not hallucination.

### [REFERENCE] `krasnovsky2025eics`
Anatoly A. Krasnovsky, 2025. *Measuring Uncertainty in Transformer Circuits with Effective Information Consistency*. arXiv:2509.07149.  
URL: <https://arxiv.org/abs/2509.07149>  
Topic: sheaves x interpretability / hallucination · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2509.07149

- **Summary.** Proposes the Effective-Information Consistency Score (EICS). It combines a normalised sheaf inconsistency, computed from local Jacobians and activations of a circuit, with a Gaussian effective-information proxy for causal emergence, as a white-box uncertainty or hallucination indicator. Empirical validation on LLM tasks is explicitly deferred.
- **Why it matters for us.** A sheaf-based, white-box hallucination signal. It complements Will's black-box output-level test. It has no experiments yet, so it is weak as evidence.

### [REFERENCE] `mahadevan2025topos`
Sridhar Mahadevan, 2025. *Topos Theory for Generative AI and LLMs*. arXiv:2508.08293.  
URL: <https://arxiv.org/abs/2508.08293>  
Topic: CT x LLM / theory · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2508.08293 (author and affiliation shown in the PDF listing)

- **Summary.** Argues that the category of LLMs, viewed as functions, forms a topos, and uses that structure (including Yoneda-style universal constructions) to propose compositional generative-AI architectures. 30 pages, theoretical.
- **Why it matters for us.** A recent "LLMs as objects of a category" position with no empirical hallucination content. Useful for related work on "Yoneda / topos views of LLMs".

### [REFERENCE] `chen2023featurecomplexity`
Chen, Zhou, Yan (first names not shown in the listing), 2023. *Going Beyond Neural Network Feature Similarity: The Network Feature Complexity and Its Interpretation Using Category Theory*. arXiv:2310.06756.  
URL: <https://arxiv.org/abs/2310.06756>  
Topic: CT x representations / naturality --- · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/2310.06756 (author surnames only, from the search summary)

- **Summary.** Models a network as a category with its parameters as a functor. Two features are functionally equivalent when there is a natural transformation between the corresponding functors. Feature redundancy and complexity are studied through natural transformations from a functor to itself.
- **Why it matters for us.** The clearest "natural transformations as representation equivalence" paper. It suggests a naturality-based (not just functoriality-based) consistency test for LLMs, such as paraphrase-invariance as naturality.


## Cluster C: Sheaves, cohomology, contextuality & consistency

### [READ-FIRST] `hansen2019spectral`
Jakob Hansen, Robert Ghrist, 2019. *Toward a Spectral Theory of Cellular Sheaves*. Journal of Applied and Computational Topology 3:315–358. arXiv:1808.01513.  
URL: <https://arxiv.org/abs/1808.01513>  
Topic: sheaf Laplacian foundations · Depth read: abstract+method(secondary)  
Checked against: WebSearch listing of https://arxiv.org/pdf/1808.01513, https://alphaxiv.org/abs/1808.01513, https://doi.org/10.1007/s41468-019-00038-7

- **Summary.** This paper is the foundational reference for sheaf Laplacians. It defines the coboundary δ: C^0→C^1 for a cellular sheaf on a cell complex and the Hodge-style Laplacian L_F = δ^T δ, whose kernel is H^0, the space of global sections. It then extends spectral graph theory to sheaves (eigenvalue interlacing, sparsification, effective resistance, harmonic extension, sheaf approximation), and with constant sheaves it reduces to the ordinary graph Laplacian.
- **Why it matters for us.** This is the canonical definition to implement. The Dirichlet energy x^T L_F x = Σ_e ||(δx)_e||² generalizes delta_comp from one chain to an arbitrary DAG or graph of sub-question answers.

### [READ-FIRST] `gebhart2023knowledge`
Thomas Gebhart, Jakob Hansen, Paul Schrater, 2023. *Knowledge Sheaves: A Sheaf-Theoretic Framework for Knowledge Graph Embedding*. AISTATS 2023, PMLR 206:9094–9116. arXiv:2110.03789.  
URL: <https://proceedings.mlr.press/v206/gebhart23a.html>  
Topic: knowledge graphs / sheaves · Depth read: abstract+method(secondary)  
Checked against: WebSearch listing of https://proceedings.mlr.press/v206/gebhart23a.html, https://arxiv.org/abs/2110.03789v2, https://virtual.aistats.org/virtual/2023/poster/5466

- **Summary.** A knowledge sheaf is a cellular sheaf on the KG *schema* Q, with entity-type stalks and relation restriction maps. A KG embedding is a 0-cochain that is an approximate global section, and many KGE losses (e.g. TransE, when the restriction maps are identity) are sheaf-consistency (Laplacian-energy) losses. **Composite or multi-hop relations are answered by harmonic extension** with respect to the sheaf Laplacian, without special training.
- **Why it matters for us.** This is the closest existing formalism to our setting. A multi-hop chain x→y→z is a path in a knowledge sheaf, and "direct vs. stepwise" corresponds to comparing a composite restriction with harmonic extension along the path. Their composite-query machinery is the obvious template for generalizing delta_comp to DAGs.

### [READ-FIRST] `robinson2020assignments`
Michael Robinson, 2020. *Assignments to sheaves of pseudometric spaces*. Compositionality 2:2. arXiv:1805.08927.  
URL: <https://compositionality.episciences.org/13508>  
Topic: sheaf data fusion / consistency radius · Depth read: abstract+method(secondary)  
Checked against: WebSearch listing of https://compositionality.episciences.org/13508, https://arxiv.org/abs/1805.08927v6

- **Summary.** Stalks are pseudometric spaces, and an *assignment* puts a value on some or all cells. The **consistency radius** is the supremum over all restriction relations of the distance between a restricted value and the value assigned downstream. It is zero exactly for global sections, it is continuous, and it is stable under small perturbations of the data or the sheaf. Thresholding it gives a *consistency filtration* of open covers, a functorial, persistence-like summary of *where* the data are consistent.
- **Why it matters for us.** This is the right generalization of delta_comp because it works with **arbitrary metrics** such as total variation between answer distributions, with no linear algebra needed. The consistency filtration localizes *which* sub-questions fail to glue, which is what a budgeted verifier needs.

### [READ-FIRST] `abramsky2011sheaf`
Samson Abramsky, Adam Brandenburger, 2011. *The sheaf-theoretic structure of non-locality and contextuality*. New Journal of Physics 13:113036. arXiv:1102.0264.  
URL: <https://arxiv.org/abs/1102.0264>  
Topic: contextuality / sheaf obstructions · Depth read: abstract+method(secondary, plus my own knowledge of the framework: flagged in Key definitions)  
Checked against: WebSearch listing of https://arxiv.org/abs/1102.0264v1, https://www.cs.ox.ac.uk/publications/publication7961-abstract.html

- **Summary.** Measurement scenarios are modelled by a covering family of contexts. Empirical models are compatible families of local distributions over the outcome sheaf. Contextuality is *exactly* the non-existence of a global section, i.e. no joint distribution that marginalizes to every local one. Non-locality is a special case, and the paper gives a strict hierarchy (probabilistic < possibilistic < strong contextuality).
- **Why it matters for us.** It formalizes "local answers each fine, but no globally consistent answer" for *probability distributions*, which is exactly our object (answer distributions per sub-question). It also says that our delta_comp ≠ 0 is a *compatibility* (marginal-agreement) failure, which is a weaker precondition than contextuality. That distinction should be made explicit in our writing.

### [RECOMMENDED] `hansen2021opinion`
Jakob Hansen, Robert Ghrist, 2021. *Opinion Dynamics on Discourse Sheaves*. SIAM Journal on Applied Mathematics (arXiv:2005.12798, 2020). (The venue comes from my knowledge and from Ghrist's preprint listing. The search result confirmed only the arXiv details.)  
URL: <https://arxiv.org/abs/2005.12798>  
Topic: sheaf Laplacian dynamics / consensus · Depth read: abstract  
Checked against: WebSearch listing of https://alphaxiv.org/abs/2005.12798, https://ar5iv.arxiv.org/html/2005.12798, https://www2.math.upenn.edu/~ghrist/preprints/opinion.pdf

- **Summary.** Agents hold private opinions in vertex stalks and express them on edges through restriction maps (the "discourse sheaf"). Sheaf-Laplacian diffusion dx/dt = −L_F x converges to a harmonic state, in which expressed opinions agree with neighbours while private opinions may still differ. The paper also models selective disclosure and lying, along with bounded confidence, controllability and harmonic extension.
- **Why it matters for us.** It gives a ready model of claims that agree on what is shared but differ privately. The restriction map is the projection of a full answer onto the sub-question shared by two reasoning steps. The paper also shows that "lying" can be encoded in the restriction maps.

### [RECOMMENDED] `hansen2020snn`
Jakob Hansen, Thomas Gebhart, 2020. *Sheaf Neural Networks*. NeurIPS 2020 Workshop on Topological Data Analysis and Beyond. arXiv:2012.06333.  
URL: <https://arxiv.org/abs/2012.06333>  
Topic: sheaf neural networks · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/2012.06333, https://alphaxiv.org/abs/2012.06333, https://mlanthology.org/neuripsw/2020/hansen2020neuripsw-sheaf

- **Summary.** The paper generalizes GCNs by replacing the graph Laplacian with a sheaf Laplacian in the diffusion/convolution step. It shows gains on signed and asymmetric relations, using synthetic semi-supervised node classification on signed graphs.
- **Why it matters for us.** Signed graphs are the simplest case where "agree vs. contradict" between claims is encoded in the restriction maps (+1/−1). That fits support/contradiction edges in a claim DAG directly.

### [RECOMMENDED] `bodnar2022nsd`
Cristian Bodnar, Francesco Di Giovanni, Benjamin Paul Chamberlain, Pietro Liò, Michael M. Bronstein, 2022. *Neural Sheaf Diffusion: A Topological Perspective on Heterophily and Oversmoothing in GNNs*. NeurIPS 2022. arXiv:2202.04579.  
URL: <https://arxiv.org/abs/2202.04579>  
Topic: sheaf neural networks · Depth read: abstract+method(secondary)  
Checked against: WebSearch listing of https://arxiv.org/abs/2202.04579v4, https://papers.neurips.cc/paper_files/paper/2022/hash/75c45fca2aa416ada062b26cc4fb7641-Abstract-Conference.html

- **Summary.** The paper argues that standard GNNs implicitly use the trivial sheaf, and that this causes oversmoothing and failure on heterophilic graphs. It learns non-trivial restriction maps from node features and runs discretized sheaf diffusion with them. Diagonal, orthogonal and general restriction-map families give increasing control over where the diffusion converges. Code: github.com/twitter-research/neural-sheaf-diffusion.
- **Why it matters for us.** It is the reference implementation for *learning* restriction maps F_{v⊴e} = Φ(x_v, x_u) from features. We would need that if the "projection onto the shared sub-question" is learned from embeddings rather than hand-specified.

### [RECOMMENDED] `robinson2017sensor`
Michael Robinson, 2017. *Sheaves are the canonical data structure for sensor integration*. Information Fusion 36:208–224. arXiv:1603.01446.  
URL: <https://arxiv.org/abs/1603.01446>  
Topic: sheaf data fusion / consistency radius · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/1603.01446, https://alphaxiv.org/abs/1603.01446, https://www.sciencedirect.com/science/article/am/pii/S156625351630207X

- **Summary.** The paper argues that sheaves are the canonical model for fusing heterogeneous sensors. It gives a sensor-agnostic consistency measure, a fusion procedure (finding the nearest global section) and detection of systemic blind spots. The model (the sheaf) is kept separate from the data (the assignment).
- **Why it matters for us.** The model/data split maps directly onto our setup. The question DAG and its compositional constraints form the sheaf, and the LLM's answers on each sub-question form the assignment. "Fusion" is the global answer most consistent with all local answers.

### [RECOMMENDED] `abramsky2015contextuality`
Samson Abramsky, Rui Soares Barbosa, Kohei Kishida, Raymond Lal, Shane Mansfield, 2015. *Contextuality, Cohomology and Paradox*. CSL 2015, LIPIcs 41:211–228. arXiv:1502.03097.  
URL: <https://doi.org/10.4230/LIPIcs.CSL.2015.211>  
Topic: contextuality / sheaf obstructions · Depth read: abstract  
Checked against: WebSearch listing of https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CSL.2015.211, https://arxiv.org/abs/1502.03097v1

- **Summary.** The paper extends sheaf-theoretic contextuality beyond physics, including to databases. It shows that logical paradoxes (Liar cycles) have the same "locally consistent, globally inconsistent" structure, and that "All-vs-Nothing" contextuality proofs are witnessed by Čech-cohomological obstructions (nonzero classes in H^1).
- **Why it matters for us.** It is the precise bridge from "contradictory cycle of claims" to "H^1 ≠ 0". A cycle of LLM claims that is locally pairwise consistent but globally contradictory is a Liar-cycle-like object, and cohomology can certify it.

### [RECOMMENDED] `lo2025contextualityllm`
Kin Ian Lo, Mehrnoosh Sadrzadeh, Shane Mansfield, 2024/2025. *Quantum-Like Contextuality in Large Language Models*. arXiv:2412.16806. Journal version listed in Proceedings of the Royal Society A (DOI 10.1098/rspa.2024.0399). The journal details come from an aggregator and a Royal Society URL in the search results and were not directly checked.  
URL: <https://arxiv.org/abs/2412.16806>  
Topic: contextuality x LLMs · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2412.16806, https://royalsocietypublishing.org/rspa/article/481/2319/20240399/234330/Quantum-like-contextuality-in-large-language

- **Summary.** The authors instantiate a contextuality scenario schema with ~52M natural-language instances and read the distributions off BERT's masked-word probabilities. Natural-language data are *signalling* (the marginals don't agree), so they use a signalling-corrected sheaf-theoretic measure and Contextuality-by-Default. Results: 0.148% sheaf-contextual vs. 71.1% CbD-contextual.
- **Why it matters for us.** This is the only verified work that applies Abramsky–Brandenburger machinery to language-model *output distributions*. It also flags that LM marginals disagree between contexts (signalling), which is exactly what delta_comp measures. So delta_comp is a signalling measure, and genuine contextuality is a separate, rarer phenomenon.

### [RECOMMENDED] `kim2025holograph`
Hyunjun Kim, 2025. *HOLOGRAPH: Active Causal Discovery via Sheaf-Theoretic Alignment of Large Language Model Priors*. arXiv:2512.24478.  
URL: <https://arxiv.org/abs/2512.24478>  
Topic: sheaves x LLMs · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2512.24478v2, https://arxiv.org/html/2512.24478

- **Summary.** The paper treats an LLM's local causal beliefs (over variable subsets) as sections of a presheaf and searches for a global section, a coherent causal graph, that reconciles potentially contradictory LLM answers. Active queries are chosen to reduce the remaining inconsistency.
- **Why it matters for us.** This is a direct precedent for "local LLM answers on overlapping sub-problems → glue → measure the failure → choose next queries". It is close to the parent project's budgeted verification framing, so there is **novelty risk on the active-query side**. It is single-author and not peer reviewed.

### [REFERENCE] `hansen2020thesis`
Jakob Hansen, 2020. *Laplacians of Cellular Sheaves: Theory and Applications*. PhD thesis, University of Pennsylvania (Penn Dissertations 4156; advisor R. Ghrist).  
URL: <https://repository.upenn.edu/edissertations/4156>  
Topic: sheaf Laplacian foundations · Depth read: abstract  
Checked against: WebSearch listing of https://repository.upenn.edu/edissertations/4156, https://core.ac.uk/download/479136918.pdf

- **Summary.** The thesis gives a consolidated treatment of Hodge Laplacians of cellular sheaves, sheaf approximation, sheaf expanders, and applications to opinion dynamics, learning sheaves from data, linear control and distributed optimization.
- **Why it matters for us.** It is the single best long-form reference for implementation details: normalized Laplacians, harmonic extension, and learning restriction maps from data.

### [REFERENCE] `curry2014sheaves`
Justin Curry, 2014. *Sheaves, Cosheaves and Applications*. PhD thesis, University of Pennsylvania. arXiv:1303.3255.  
URL: <https://arxiv.org/abs/1303.3255>  
Topic: sheaf foundations · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/1303.3255 (and citation in "Persistent sheaf cohomology", https://arxiv.org/pdf/2204.13446)

- **Summary.** This is the standard thesis on cellular sheaves and cosheaves over cell complexes. A cellular sheaf there is a finite family of vector spaces and maps indexed by the face poset. The thesis covers cellular sheaf cohomology, level-set persistence through constructible cosheaves, and a van Kampen theorem.
- **Why it matters for us.** It is the rigorous source for "cellular sheaf = functor from the face poset to Vect" and for computing cellular sheaf cohomology. Use it if we go beyond graphs to higher cells, for example a 2-cell for each triangle of mutually overlapping sub-questions.

### [REFERENCE] `barbero2022connection`
Federico Barbero, Cristian Bodnar, Haitz Sáez de Ocáriz Borde, Michael Bronstein, Petar Veličković, Pietro Liò, 2022. *Sheaf Neural Networks with Connection Laplacians*. Proceedings of Topological, Algebraic, and Geometric Learning Workshops 2022, PMLR 196. arXiv:2206.08702.  
URL: <https://proceedings.mlr.press/v196/barbero22a.html>  
Topic: sheaf neural networks · Depth read: abstract  
Checked against: WebSearch listing of https://proceedings.mlr.press/v196/barbero22a.html, https://arxiv.org/pdf/2206.08702

- **Summary.** The sheaf is computed non-parametrically rather than learned: orthogonal restriction maps align local tangent spaces (local PCA) of neighbouring points, which gives a connection Laplacian. It matches or beats learned NSD at lower training cost.
- **Why it matters for us.** It shows a cheap, training-free way to build restriction maps from embedding geometry. That could serve as a baseline sheaf over LLM hidden-state or answer embeddings.

### [REFERENCE] `barbero2022sheafattention`
Federico Barbero, Cristian Bodnar, Haitz Sáez de Ocáriz Borde, Pietro Liò (+ possibly Michael Bronstein, Petar Veličković; author lists differ between sources), 2022. *Sheaf Attention Networks*. NeurIPS 2022 Workshop (GLFrontiers).  
URL: <https://mlanthology.org/neuripsw/2022/barbero2022neuripsw-sheaf>  
Topic: sheaf neural networks · Depth read: abstract  
Checked against: WebSearch listing of https://neurips.cc/virtual/2022/60824, https://mlanthology.org/neuripsw/2022/barbero2022neuripsw-sheaf

- **Summary.** The paper generalizes GAT-style attention to cellular sheaves (SheafAN). It consistently outperforms GAT and reduces oversmoothing on heterophilic graphs.
- **Why it matters for us.** This is peripheral. Read it only if we build a learned model over claim graphs. **The author list is not fully verified; check it before citing.**

### [REFERENCE] `abramsky2013relational`
Samson Abramsky, 2013. *Relational Databases and Bell's Theorem*. In: In Search of Elegance in the Theory and Practice of Computation (Festschrift for Peter Buneman), LNCS 8000, pp. 13–35, Springer. arXiv:1208.6416.  
URL: <https://arxiv.org/abs/1208.6416>  
Topic: contextuality / databases · Depth read: abstract  
Checked against: WebSearch listing of https://www.arxiv.org/abs/1208.6416, https://researchr.org/publication/Abramsky13-1

- **Summary.** Whether an empirical model has a local hidden-variable explanation is equivalent to whether a database instance (a family of relations on overlapping attribute sets) admits a universal relation. The paper also gives a common algebraic language for relational, probabilistic databases and contextuality.
- **Why it matters for us.** Treat each sub-question's answer table as a relation on its variables (entities x, y, z). Global consistency of an LLM's reasoning then becomes the existence of a universal relation, which is the database-theory version of gluing and is directly computable for small DAGs.

### [REFERENCE] `hanks2025distributed`
Tyler Hanks, Hans Riess, Samuel Cohen, Trevor Gross, Matthew Hale, James Fairbanks, 2025. *Distributed Multi-agent Coordination over Cellular Sheaves*. arXiv:2504.02049. (**Note: Ghrist is not an author**, contrary to the task brief.)  
URL: <https://arxiv.org/abs/2504.02049>  
Topic: multi-agent consensus · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/abs/2504.02049, https://arxiv.org/html/2504.02049v2

- **Summary.** Agents' states live in vertex stalks, and coordination goals (consensus, formation, flocking) are encoded as nonlinear edge potentials on sheaf edge stalks. These "nonlinear homological programs" are solved with a distributed ADMM.
- **Why it matters for us.** It gives a template for *nonlinear* edge potentials, e.g. TV distance or KL between answer distributions instead of ||·||², while keeping a sheaf-Laplacian-like structure. It also gives a distributed solver for finding the most consistent global assignment.

### [REFERENCE] `grant2026gluing`
Bryce Grant, Peng Wang, 2026. *Gluing Local Contexts into Global Meaning: A Sheaf-Theoretic Decomposition of Transformer Representations*. ICLR 2026 Workshop on Unifying Concept Representation Learning (non-archival); arXiv:2610.17117.  
URL: <https://arxiv.org/abs/2610.17117>  
Topic: sheaves x LLMs · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/pdf/2610.17117, https://cwru-aism.github.io/gluing-lc-page/

- **Summary.** The paper builds a cellular sheaf whose edges are paraphrase/context relations over frozen transformer activations. It uses the sheaf Laplacian to split representations into a context-stable (H^0, "content") subspace and a context-dependent (H^1-like) part, evaluated on STS-B-style similarity.
- **Why it matters for us.** This is the most recent sheaf-Laplacian-on-LLM work found. It operates on *representations*, not on answer-level consistency or hallucination, but it shows the venue appetite and is the closest "sheaf Laplacian x LLM" paper. **The venue is inconsistent across sources (ICLR 2026 workshop vs. a NeurIPS 2026 poster listing), so check it before citing.**

### [REFERENCE] `bazarova2025toha`
Alexandra Bazarova, Aleksandr Yugay, Andrey Shulga, Alina Ermilova, …, Alexey Zaytsev (13 authors), 2025/2026. *Hallucination Detection in LLMs with Topological Divergence on Attention Graphs* (TOHA). arXiv:2504.10063; ACL 2026 (long).  
URL: <https://arxiv.org/abs/2504.10063>  
Topic: TDA x hallucination · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/html/2504.10063v2, https://preview.aclanthology.org/ingest-acl/2026.acl-long.704/

- **Summary.** TOHA is a training-free RAG hallucination detector. It compares the topology (via a topological-divergence / MST-based persistence summary) of prompt and response subgraphs of attention graphs, averaged over a few "hallucination-aware" heads that transfer across datasets.
- **Why it matters for us.** This is the main TDA-for-hallucination baseline. It is white-box and attention-based, whereas our signal is black-box and distribution-based, so the two are complementary.

### [REFERENCE] `samaga2026halluzig`
Shreyas N. Samaga, Gilberto Gonzalez Arroyo, Tamal K. Dey, 2026. *HalluZig: Hallucination Detection using Zigzag Persistence*. EACL 2026 (long), pp. 3466–3482. arXiv:2601.01552.  
URL: <https://aclanthology.org/2026.eacl-long.159>  
Topic: TDA x hallucination · Depth read: abstract  
Checked against: WebSearch listing of https://aclanthology.org/2026.eacl-long.159, https://arxiv.org/abs/2601.01552v2

- **Summary.** The layer-wise attention matrices form a zigzag graph filtration, and zigzag persistence summaries become hallucination-detection features. They transfer across models and work from only the first ~70% of layers.
- **Why it matters for us.** This is a second TDA baseline. Zigzag persistence over *reasoning steps* (rather than layers) is a possible extension for stepwise chains.

### [REFERENCE] `schmid2025prospectus`
Eric Schmid, 2025. *Applied Sheaf Theory For Multi-agent Artificial Intelligence (Reinforcement Learning) Systems: A Prospectus*. arXiv:2504.17700.  
URL: <https://arxiv.org/abs/2504.17700>  
Topic: tutorial / multi-agent --- · Depth read: abstract  
Checked against: WebSearch listing of https://arxiv.org/html/2504.17700v1, https://www.emergentmind.com/papers/2504.17700

- **Summary.** A pedagogical introduction to sheaf cohomology for CS/AI readers, followed by a research prospectus on sheaf-Laplacian consensus in multi-agent RL.
- **Why it matters for us.** It is useful as an accessible tutorial for Will. It contains no LLM content.


## Cluster D: Causal abstraction, mechanistic interpretability & representation structure

### [READ-FIRST] `rischel2021compositional`
Eigil F. Rischel, Sebastian Weichwald, 2021. *Compositional Abstraction Error and a Category of Causal Models*. UAI 2021, PMLR 161:1013-1023.  
URL: <https://proceedings.mlr.press/v161/rischel21a.html>  
Topic: causal abstraction / category theory · Depth read: abstract + method snippets  
Checked against: WebSearch results listing proceedings.mlr.press/v161/rischel21a.html and arxiv.org/abs/2103.15758, plus mlanthology

- **Summary.** The paper builds a category of finite interventional causal models in which abstractions are morphisms. Each abstraction gets an error, the worst-case Jensen-Shannon distance by which the abstraction/intervention square fails to commute. Using enriched category theory (FinStoch enriched in Met), it proves that the error of a composite abstraction is bounded by the sum of the errors of its steps. It also extends Rubenstein et al. (2017) to inexact transformations.
- **Why it matters for us.** This is the closest existing template for "functoriality error". A non-commuting square with a metric-valued defect is the same thing as your direct-vs-stepwise 2-hop disagreement, and their subadditivity bound is the kind of theorem you could state for chained relations.

### [READ-FIRST] `geiger2025causal`
Atticus Geiger, Duligur Ibeling, Amir Zur, Maheep Chaudhary, Sonakshi Chauhan, Jing Huang, Aryaman Arora, Zhengxuan Wu, Noah Goodman, Christopher Potts, Thomas Icard, 2025. *Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability*. JMLR 26(83):1-64. (arXiv 2301.04709, first titled "Causal Abstraction for Faithful Model Interpretation")  
URL: <https://www.jmlr.org/papers/v26/23-0058.html>  
Topic: causal abstraction for NNs · Depth read: abstract + snippets  
Checked against: WebSearch results (jmlr.org v26/23-0058, arxiv.org/abs/2301.04709)

- **Summary.** The paper generalises causal abstraction to arbitrary mechanism transformations, including cyclic models and multi-source interventions, and defines approximate abstraction with graded faithfulness. It formalises polysemanticity and the linear representation hypothesis inside this theory. It then shows that activation patching, path patching, causal mediation, DAS, SAEs, probing and others are special cases.
- **Why it matters for us.** This is the unifying theory you would map onto categorical language. Abstraction maps already compose, and approximate abstraction is the quantity a "functoriality score" would be measuring.

### [READ-FIRST] `hernandez2024linearity`
Evan Hernandez, Arnab Sen Sharma, Tal Haklay, Kevin Meng, Martin Wattenberg, Jacob Andreas, Yonatan Belinkov, David Bau, 2024. *Linearity of Relation Decoding in Transformer Language Models*. ICLR 2024. (arXiv:2308.09124)  
URL: <https://arxiv.org/abs/2308.09124>  
Topic: linear relational structure · Depth read: abstract + method snippets (see Key method details)  
Checked against: WebSearch results (proceedings.iclr.cc 2024 hash 2b6d7285...; arxiv.org/pdf/2308.09124; lre.baulab.info)

- **Summary.** For many relations, the LM's map from a subject representation s to the object prediction is well approximated by an affine map LRE_r(s) = βW_r s + b_r. W_r and b_r come from a first-order Taylor expansion, averaging the Jacobian and bias over a few examples. Roughly half of 47 relations are faithfully linear. Others (for example company CEO) are encoded accurately but not linearly.
- **Why it matters for us.** This is the most directly usable tool. Each relation becomes a matrix, so a 2-hop question becomes a composition W_g W_f that can be compared against both the model's direct 2-hop answer and the stepwise answer. Functoriality becomes a linear-algebra measurement.

### [RECOMMENDED] `otsuka2022equivalence`
Jun Otsuka, Hayato Saigo, 2022. *On the Equivalence of Causal Models: A Category-Theoretic Approach*. CLeaR 2022, PMLR 177:634-646.  
URL: <https://proceedings.mlr.press/v177/otsuka22a.html>  
Topic: causal abstraction / category theory · Depth read: abstract  
Checked against: WebSearch results listing PMLR v177 and arxiv.org/abs/2201.06981

- **Summary.** Building on Jacobs et al. (2019), causal models are treated as functors out of a syntactic category generated by a DAG. "Phi-abstraction" and "Phi-equivalence" are defined by natural transformations between such functors, for DAGs that are homomorphic. If one model is a Phi-abstraction of another, intervention calculus translates consistently between them. A condition for when an abstraction exists is given for deterministic maps.
- **Why it matters for us.** It explicitly writes abstraction as a natural transformation, which is the "interchange interventions as naturality" idea in finished form for causal models.

### [RECOMMENDED] `beckers2019abstracting`
Sander Beckers, Joseph Y. Halpern, 2019. *Abstracting Causal Models*. AAAI 2019, 33(01):2678-2685.  
URL: <https://arxiv.org/abs/1812.03789>  
Topic: causal abstraction · Depth read: abstract  
Checked against: WebSearch results (ojs.aaai.org/index.php/AAAI/article/view/4117; arxiv.org/abs/1812.03789v4; cs.cornell.edu PDF)

- **Summary.** The paper gives a hierarchy of abstraction notions of increasing strength: exact transformation, uniform transformation, abstraction, strong abstraction, and constructive abstraction. It shows that aggregating micro-variables into macro-variables is a strong abstraction.
- **Why it matters for us.** It gives you the vocabulary for how strong a model-to-model map has to be before "the LLM's internal process implements the 2-hop composition" means something.

### [RECOMMENDED] `geiger2021causal`
Atticus Geiger, Hanson Lu, Thomas Icard, Christopher Potts, 2021. *Causal Abstractions of Neural Networks*. NeurIPS 2021.  
URL: <https://arxiv.org/abs/2106.02997>  
Topic: causal abstraction for NNs · Depth read: abstract + snippets  
Checked against: WebSearch results (papers.nips.cc 2021 hash 4f5c422f..., arxiv.org/abs/2106.02997)

- **Summary.** Network components are aligned to variables of an interpretable causal model, and the alignment is tested with interchange interventions. On MQNLI, a BERT model partly realizes the reference causal model and an LSTM does not.
- **Why it matters for us.** Interchange interventions are a direct empirical test of whether a hypothesised compositional structure (hop 1 then hop 2) is causally realised inside the model.

### [RECOMMENDED] `geiger2024finding`
Atticus Geiger, Zhengxuan Wu, Christopher Potts, Thomas Icard, Noah Goodman, 2024. *Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations*. CLeaR 2024, PMLR 236:160-187.  
URL: <https://proceedings.mlr.press/v236/geiger24a.html>  
Topic: causal abstraction for NNs · Depth read: abstract + snippets  
Checked against: WebSearch results (PMLR v236 geiger24a, arxiv.org/abs/2303.02536)

- **Summary.** Distributed Alignment Search (DAS) learns a rotation of a hidden representation by gradient descent, so high-level causal variables can be aligned to subspaces in a non-standard basis instead of individual neurons. The paper reports alignments with 100% interchange intervention accuracy (IIA) on tasks where brute-force neuron alignment fails.
- **Why it matters for us.** DAS gives a trainable, quantitative method for locating a "bridge entity" subspace in 2-hop questions, with IIA as the score.

### [RECOMMENDED] `elhage2021mathematical`
Nelson Elhage, Neel Nanda, Catherine Olsson, et al. (Anthropic; Chris Olah corresponding), 2021. *A Mathematical Framework for Transformer Circuits*. Transformer Circuits Thread.  
URL: <https://transformer-circuits.pub/2021/framework/index.html>  
Topic: circuits · Depth read: abstract  
Checked against: WebSearch results (transformer-circuits.pub/2021/framework page)

- **Summary.** It analyses attention-only transformers with at most two layers. The residual stream is a shared linear communication channel, attention heads factor into QK and OV circuits, and paths compose. It introduces induction heads.
- **Why it matters for us.** Transformers decompose into sums over composed linear paths, which is the algebraic setting where "does W_g W_f approximate W_{g∘f}" is a natural question.

### [RECOMMENDED] `elhage2022toy`
Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, et al. (16 authors incl. Grosse, McCandlish, Kaplan, Amodei, Wattenberg, Olah), 2022. *Toy Models of Superposition*. Transformer Circuits Thread / arXiv:2209.10652.  
URL: <https://arxiv.org/abs/2209.10652>  
Topic: superposition · Depth read: abstract  
Checked against: WebSearch results (arxiv.org/abs/2209.10652; transformer-circuits.pub)

- **Summary.** Small ReLU models trained on sparse synthetic features store more features than they have dimensions. The paper finds phase changes, uniform-polytope geometry, and links to adversarial examples.
- **Why it matters for us.** Superposition is why linear maps between representations (LREs, stitching) are only approximate. It explains part of the functoriality defect.

### [RECOMMENDED] `christ2025structure`
Miranda Anna Christ, Adrián Csiszárik, Gergely Becsó, Dániel Varga, 2025. *The Structure of Relation Decoding Linear Operators in Large Language Models*. NeurIPS 2025. (arXiv:2510.26543)  
URL: <https://arxiv.org/abs/2510.26543>  
Topic: linear relational structure · Depth read: abstract (snippets)  
Checked against: WebSearch results (arxiv.org/abs/2510.26543v1; papers.nips.cc 2025 hash 3dada699...)

- **Summary.** Collections of Hernandez-style relation decoders compress into simple order-3 tensor networks with little loss in accuracy. This suggests linear relational decoding is mainly property-based rather than relation-specific, which explains why the decoders generalise only to semantically close relations.
- **Why it matters for us.** It is a strong caution for the "W_g W_f ≈ W_{g∘f}" idea. If LREs extract coarse properties rather than act as relation-specific maps, composition may fail for structural reasons. This is the closest prior work on the algebra of LREs.

### [RECOMMENDED] `park2024linear`
Kiho Park, Yo Joong Choe, Victor Veitch, 2024. *The Linear Representation Hypothesis and the Geometry of Large Language Models*. ICML 2024, PMLR 235:39643-39666. (arXiv:2311.03658)  
URL: <https://arxiv.org/abs/2311.03658>  
Topic: representation geometry · Depth read: abstract  
Checked against: WebSearch results (proceedings.mlr.press/v235/park24c.html; arxiv.org/abs/2311.03658)

- **Summary.** The paper formalises "linear representation" in both input (embedding) and output (unembedding) space using counterfactual pairs. It introduces a "causal inner product" under which causally separable concepts are orthogonal, estimated from the unembedding matrix, and tests this on LLaMA-2.
- **Why it matters for us.** It supplies the right inner product and geometry for measuring how far a composed map lands from the target. An LRE-composition defect should be measured in this metric, not raw Euclidean distance.

### [RECOMMENDED] `huh2024platonic`
Minyoung Huh, Brian Cheung, Tongzhou Wang, Phillip Isola, 2024. *Position: The Platonic Representation Hypothesis*. ICML 2024 (PMLR 235). (arXiv:2405.07987)  
URL: <https://arxiv.org/abs/2405.07987>  
Topic: representation similarity · Depth read: abstract  
Checked against: WebSearch results (arxiv.org/abs/2405.07987v5; ICML.cc poster 34734; mlanthology)

- **Summary.** Representations across architectures, objectives and modalities converge as scale grows, measured by the kernel (similarity structure) they induce, for example mutual-nearest-neighbour alignment.
- **Why it matters for us.** Kernel convergence is a Yoneda-flavoured claim: an object is known by its similarities to everything else. It motivates testing whether relation maps, not only kernels, agree across models.

### [RECOMMENDED] `lenc2015understanding`
Karel Lenc, Andrea Vedaldi, 2015. *Understanding Image Representations by Measuring Their Equivariance and Equivalence*. CVPR 2015, pp. 991-999. (arXiv:1411.5908; extended IJCV 2019)  
URL: <https://openaccess.thecvf.com/content_cvpr_2015/html/Lenc_Understanding_Image_Representations_2015_CVPR_paper.html>  
Topic: model comparison · Depth read: abstract  
Checked against: WebSearch results (CVF open access page; alphaxiv 1411.5908)

- **Summary.** Equivariance is how representations transform under input transformations. Equivalence is tested by stitching layers between CNNs ("Franken-CNNs").
- **Why it matters for us.** Equivariance is literally a naturality condition, and stitching layers are candidate natural transformations between network "functors".

### [RECOMMENDED] `bansal2021revisiting`
Yamini Bansal, Preetum Nakkiran, Boaz Barak, 2021. *Revisiting Model Stitching to Compare Neural Representations*. NeurIPS 2021. (arXiv:2106.07682)  
URL: <https://arxiv.org/abs/2106.07682>  
Topic: model comparison · Depth read: abstract  
Checked against: WebSearch results (proceedings.neurips.cc 2021 hash 01ded425...)

- **Summary.** A trainable stitching layer joins the bottom of one frozen model to the top of another. Good models stitch with little loss even across training regimes, "more is better" stitching occurs, and stitching connectivity holds. The method can expose differences that CKA cannot.
- **Why it matters for us.** Stitching cost is a measurable "how far from a natural isomorphism" quantity between two models' representations.

### [RECOMMENDED] `lan2024sparse`
Michael Lan, Philip Torr, Austin Meek, Ashkan Khakzar, David Krueger, Fazl Barez, 2024. *Sparse Autoencoders Reveal Universal Feature Spaces Across Large Language Models* (v4 retitled *Quantifying Feature Space Universality Across Large Language Models via Sparse Autoencoders*). arXiv:2410.06981.  
URL: <https://arxiv.org/abs/2410.06981>  
Topic: universality · Depth read: abstract (title/authors only in snippets)  
Checked against: WebSearch results (arxiv.org/abs/2410.06981v1-v4; huggingface.co/papers/2410.06981)

- **Summary.** SAE features from different LLMs are paired by activation correlation, and the resulting feature spaces are compared with representational similarity measures (SVCCA/RSA), finding substantial cross-model similarity. **(memory, confirm)** for the method details.
- **Why it matters for us.** It is a direct precursor to "SAE feature dictionaries as functors across model sizes".

### [RECOMMENDED] `meng2022locating`
Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov, 2022. *Locating and Editing Factual Associations in GPT*. NeurIPS 2022. (arXiv:2202.05262)  
URL: <https://arxiv.org/abs/2202.05262>  
Topic: factual recall · Depth read: abstract  
Checked against: WebSearch results (proceedings.nips.cc 2022 paper PDF; arxiv.org/abs/2202.05262; rome.baulab.info)

- **Summary.** Causal tracing localises factual recall to mid-layer MLPs at the last subject token. ROME makes a rank-one edit to an MLP weight to change one fact. The paper introduces the CounterFact dataset.
- **Why it matters for us.** Editing one hop (s → b) and checking whether the 2-hop answer updates is a functoriality test under intervention. Ripple-effect failures are functoriality violations.

### [RECOMMENDED] `geva2023dissecting`
Mor Geva, Jasmijn Bastings, Katja Filippova, Amir Globerson, 2023. *Dissecting Recall of Factual Associations in Auto-Regressive Language Models*. EMNLP 2023, pp. 12216-12235. (arXiv:2304.14767)  
URL: <https://aclanthology.org/2023.emnlp-main.751>  
Topic: factual recall · Depth read: abstract  
Checked against: WebSearch results (aclanthology 2023.emnlp-main.751; arxiv 2304.14767v3)

- **Summary.** Recall has three steps: the last-subject representation is enriched by early MLPs, relation information flows to the final position, and attention heads extract the attribute from the subject, often with subject-attribute mappings stored in their parameters.
- **Why it matters for us.** It gives the mechanistic decomposition of one hop. A 2-hop answer requires this pipeline to run twice, which explains why direct ≠ stepwise.

### [RECOMMENDED] `yang2024latent`
Sohee Yang, Elena Gribovskaya, Nora Kassner, Mor Geva, Sebastian Riedel, 2024. *Do Large Language Models Latently Perform Multi-Hop Reasoning?* ACL 2024 (Long), pp. 10210-10229. (arXiv:2402.16837)  
URL: <https://aclanthology.org/2024.acl-long.550>  
Topic: multi-hop · Depth read: abstract  
Checked against: WebSearch results (aclanthology 2024.acl-long.550; arxiv.org/html/2402.16837v2)

- **Summary.** The TwoHopFact dataset has 45,595 prompts across 52 composition types. There is strong evidence of the first hop (bridge-entity recall) and it scales with model size. The second hop is moderate and does not scale. Latent composition is strong for only some relation types.
- **Why it matters for us.** This is the closest empirical prior on your functoriality question, with a ready dataset. Evaluate your metric against it.

### [RECOMMENDED] `biran2024hopping`
Eden Biran, Daniela Gottesman, Sohee Yang, Mor Geva, Amir Globerson, 2024. *Hopping Too Late: Exploring the Limitations of Large Language Models on Multi-Hop Queries*. EMNLP 2024, pp. 14113-14130. (arXiv:2406.12775)  
URL: <https://aclanthology.org/2024.emnlp-main.781>  
Topic: multi-hop · Depth read: abstract  
Checked against: WebSearch results (aclanthology 2024.emnlp-main.781; arxiv 2406.12775)

- **Summary.** In 2-hop queries the bridge entity is resolved in early-to-mid layers, and the second hop runs later, sometimes too late for the layers that hold the needed knowledge. "Back-patching" the later hidden state into earlier layers fixes up to 66% of failures. A dataset of 82,020 2-hop queries is released.
- **Why it matters for us.** It gives a mechanistic reason for composition failure (layer budget) and an intervention (back-patching) that repairs it. Both can be measured alongside a functoriality score.

### [RECOMMENDED] `gauderis2026compositional`
Ward Gauderis, Thomas Dooms, Steven T. Homer, Kola Ayonrinde, Geraint A. Wiggins, 2026. *From Mechanistic to Compositional Interpretability*. arXiv:2605.08934 (ICML 2026 workshop).  
URL: <https://arxiv.org/abs/2605.08934>  
Topic: category theory + interpretability Also surfaced but not verified beyond a search hit: arXiv:2310.06756 (Chen, Zhou, Yan, "Going Beyond Neural Network Feature Similarity: ... Using Category Theory"), arXiv:2410.05353 (survey of category theory for deep learning), arXiv:2603.30002 ("Tracking Equivalent Mechanistic Interpretations Across Neural Networks"). Check these before citing. --- · Depth read: abstract (snippets)  
Checked against: WebSearch results (arxiv.org/pdf/2605.08934; icml.cc/virtual/2026/69382; computationalcreativity.net extended abstract)

- **Summary.** Syntax and semantics are separate monoidal categories linked by a representation functor S → C. An interpretation is grounded when the syntactic and semantic interpretations commute. "Compressive refinements" (functors S → S' that do not increase description length) frame interpretability as MDL optimisation, and mainstream mechanistic methods appear as special cases.
- **Why it matters for us.** This is the most explicit category-theoretic treatment of mech interp found, and it is very recent. Cite it and position your work as an empirical counterpart.

### [REFERENCE] `rubenstein2017causal`
Paul K. Rubenstein, Sebastian Weichwald, Stephan Bongers, Joris M. Mooij, Dominik Janzing, Moritz Grosse-Wentrup, Bernhard Schölkopf, 2017. *Causal Consistency of Structural Equation Models*. UAI 2017 (PMLR R15:151-160).  
URL: <https://arxiv.org/abs/1707.00819>  
Topic: causal abstraction · Depth read: abstract  
Checked against: WebSearch results (proceedings.mlr.press/r15/rubenstein-17a.html, ELLIS page, arXiv 1707.00819)

- **Summary.** This paper introduces "exact transformations" between SEMs: a map of variables and interventions under which interventional distributions commute. It covers marginalisation, micro-to-macro aggregation, and time series to equilibrium.
- **Why it matters for us.** It is the root definition that Beckers-Halpern, Rischel-Weichwald and Geiger all refine.

### [REFERENCE] `olah2020zoom`
Chris Olah, Nick Cammarata, Ludwig Schubert, Gabriel Goh, Michael Petrov, Shan Carter, 2020. *Zoom In: An Introduction to Circuits*. Distill. doi:10.23915/distill.00024.001  
URL: <https://distill.pub/2020/circuits/zoom-in/>  
Topic: circuits · Depth read: abstract  
Checked against: WebSearch results (distill.pub page, mlanthology)

- **Summary.** The essay states three claims: networks contain meaningful features, features connect through interpretable circuits, and similar features and circuits recur across models ("universality"). Examples come from InceptionV1.
- **Why it matters for us.** The universality claim is informally a claim that there are functor-like correspondences between different trained models.

### [REFERENCE] `bricken2023monosemanticity`
Trenton Bricken, Adly Templeton, Joshua Batson, Brian Chen, Adam Jermyn, et al. (Anthropic; Olah corresponding), 2023. *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning*. Transformer Circuits Thread.  
URL: <https://transformer-circuits.pub/2023/monosemantic-features/index.html>  
Topic: SAEs · Depth read: abstract  
Checked against: WebSearch results (transformer-circuits.pub/2023/monosemantic-features; anthropic.com/research page)

- **Summary.** A sparse autoencoder decomposes a 512-neuron MLP layer of a 1-layer transformer into more than 4000 largely monosemantic features.
- **Why it matters for us.** SAE features are the candidate "objects" for any cross-model functor.

### [REFERENCE] `templeton2024scaling`
Adly Templeton, Tom Conerly, et al. (Anthropic; incl. Olah, Henighan), 2024. *Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet*. Transformer Circuits Thread.  
URL: <https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html>  
Topic: SAEs · Depth read: abstract  
Checked against: WebSearch results (longtermwiki and alphaxiv entries citing transformer-circuits; content consistent). Note: search also showed a 2026 arXiv posting 2605.29358 under this title. I did not use that ID.

- **Summary.** SAEs with up to 34M features are trained on Claude 3 Sonnet's middle-layer residual stream. They yield abstract, multilingual and multimodal features, including safety-relevant ones (deception, sycophancy, backdoors), which steer behaviour when clamped.
- **Why it matters for us.** It shows that SAE features are causally usable safety handles, which is what you would want to transport across models.

### [REFERENCE] `cunningham2024sparse`
Hoagy Cunningham, Aidan Ewart, Logan Riggs (Smith), Robert Huben, Lee Sharkey, 2024. *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. ICLR 2024. (arXiv:2309.08600)  
URL: <https://arxiv.org/abs/2309.08600>  
Topic: SAEs · Depth read: abstract  
Checked against: WebSearch results (proceedings.iclr.cc 2024 hash 1fa1ab11...; huggingface.co/papers/2309.08600). Author order differs between the ICLR and arXiv versions.

- **Summary.** SAEs on LM activations produce features that are more interpretable than PCA/ICA/neuron baselines. On IOI they locate causally responsible features at finer resolution than earlier decompositions.
- **Why it matters for us.** This is the open-model SAE baseline (Pythia) that you can actually reproduce.

### [REFERENCE] `mikolov2013linguistic`
Tomas Mikolov, Wen-tau Yih, Geoffrey Zweig, 2013. *Linguistic Regularities in Continuous Space Word Representations*. NAACL-HLT 2013, pp. 746-751.  
URL: <https://aclanthology.org/N13-1090/>  
Topic: representation geometry · Depth read: abstract  
Checked against: WebSearch results (aclanthology.org/N13-1090; microsoft.com research page)

- **Summary.** RNN-LM word vectors encode relations as constant vector offsets, for example king − man + woman ≈ queen.
- **Why it matters for us.** This is the historical origin of "relations as translations". LREs generalise the offset to an affine map, and composing offsets is trivially functorial, which LREs need not be.

### [REFERENCE] `kornblith2019similarity`
Simon Kornblith, Mohammad Norouzi, Honglak Lee, Geoffrey Hinton, 2019. *Similarity of Neural Network Representations Revisited*. ICML 2019, PMLR 97:3519-3529. (arXiv:1905.00414)  
URL: <https://arxiv.org/abs/1905.00414>  
Topic: model comparison · Depth read: abstract  
Checked against: WebSearch results (research.google pubs page; icml.cc poster 4185; arxiv 1905.00414)

- **Summary.** The paper introduces centered kernel alignment (CKA) for comparing representations. It argues that measures invariant to invertible linear transformations fail when dimension exceeds the number of datapoints. CKA identifies corresponding layers across seeds.
- **Why it matters for us.** This is the standard baseline similarity measure. It compares objects but not morphisms, which is the gap a categorical approach fills.

### [REFERENCE] `thasarathan2025universal`
Harrish Thasarathan, Julian Forsyth, Thomas Fel, Matthew Kowal, Konstantinos Derpanis, 2025. *Universal Sparse Autoencoders: Interpretable Cross-Model Concept Alignment*. ICML 2025, PMLR 267. (arXiv:2502.03714)  
URL: <https://arxiv.org/abs/2502.03714>  
Topic: universality · Depth read: abstract  
Checked against: WebSearch results (proceedings.mlr.press/v267/thasarathan25a.html; arxiv 2502.03714v1)

- **Summary.** A single overcomplete SAE encodes activations from any of several vision models and decodes to any other, so a shared concept dictionary is learned end to end.
- **Why it matters for us.** The shared dictionary is effectively a common "base category" with encoder/decoder maps to each model, a span or cospan construction you can phrase categorically.


## Cluster E: Open games, categorical cybernetics, agent foundations & formal safety

### [READ-FIRST] `capucci2021foundations`
Capucci, M., Gavranović, B., Hedges, J., Rischel, E. F., 2022. *Towards Foundations of Categorical Cybernetics*. EPTCS 372 (ACT 2021), pp. 235–248. arXiv:2105.06332.  
URL: <https://arxiv.org/abs/2105.06332>  
Topic: categorical cybernetics · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2105.06332v1 and https://arxiv.org/pdf/2105.06332

- **Summary.** This is a single categorical framework, built on parametrised optics, for processes that interact bidirectionally with an environment and with a controller. Gradient-based "open learners" and open-games-style game theory are both instances. The authors argue "cybernetic" is the right name for these processes.
- **Why it matters for us.** This is the unifying vocabulary (Para + Optic) that makes "LLM + verifier + budget controller" a single composable object. It is the right entry point to the categorical-cybernetics school.

### [READ-FIRST] `burns2022ccs`
Burns, C., Ye, H., Klein, D., Steinhardt, J., 2022. *Discovering Latent Knowledge in Language Models Without Supervision*. arXiv:2212.03827 (ICLR 2023 *(venue unverified)*).  
URL: <https://arxiv.org/abs/2212.03827>  
Topic: ELK / latent knowledge --- · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2212.03827 and https://arxiv.org/html/2212.03827v2

- **Summary.** Contrast-Consistent Search (CCS) finds a direction in activations such that a statement and its negation get complementary probabilities, i.e. **negation consistency** p(x⁺) ≈ 1 − p(x⁻) plus confidence, with no labels. It beats zero-shot by about 4% on average across 6 models and 10 datasets, halves prompt sensitivity, and stays accurate when the model is prompted to lie.
- **Why it matters for us.** The CCS loss is a functoriality constraint for a single logical operation: truth assignment should commute with negation. Will's tests generalise this from ¬ to composition of relations (multi-hop). This is the closest mainstream-safety precedent for "consistency as a label-free truth signal".

### [RECOMMENDED] `ghani2018compositional`
Ghani, N., Hedges, J., Winschel, V., Zahn, P., 2018. *Compositional Game Theory*. LICS 2018, pp. 472–481. arXiv:1603.04641.  
URL: <https://arxiv.org/abs/1603.04641>  
Topic: open games · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/1603.04641 and https://pureportal.strath.ac.uk/en/publications/compositional-game-theory/

- **Summary.** The paper introduces *open games* as morphisms of a symmetric monoidal category. Games compose sequentially by categorical composition and in parallel by the monoidal product, and string diagrams depict them. Many classical games encode faithfully, keeping their Nash equilibria and off-equilibrium best responses. "Coutility" is the utility a game returns to its environment.
- **Why it matters for us.** This is the root paper for the bidirectional (forward play / backward utility) pattern that the lens and optic literature generalises. Any "claim-DAG with backward feedback" design could be framed as an open game.

### [RECOMMENDED] `hedges2022value`
Hedges, J., Rodríguez Sakamoto, R., 2023. *Value Iteration is Optic Composition*. EPTCS 380 (ACT 2022), pp. 417–432. arXiv:2206.04547.  
URL: <https://arxiv.org/abs/2206.04547>  
Topic: categorical cybernetics / RL · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/pdf/2206.04547 and https://strathprints.strath.ac.uk/88746

- **Summary.** Value improvement is precomposition with an optic, so it is a representable functor on optics. The optimal value function is the limit of a chain of optic compositions. Examples are gridworld, inverted pendulum and a savings problem.
- **Why it matters for us.** It is a worked template for turning a dynamic-programming recursion into a categorical composition law. Budgeted claim-DAG verification is itself a DP over a DAG.

### [RECOMMENDED] `bakirtzis2022mdp`
Bakirtzis, G., Savvas, M., Topcu, U., 2025. *Categorical Semantics of Compositional Reinforcement Learning*. JMLR 26. arXiv:2208.13687.  
URL: <https://arxiv.org/abs/2208.13687>  
Topic: categorical RL / safety · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2208.13687v3 and https://jmlr.org/papers/v26/24-0197.html

- **Summary.** The paper defines a category **MDP** with fibre products and pushouts. These unify puncturing hazardous states (a safety constraint) and state–action symmetry. It gives sufficient conditions under which learning-by-parts yields the globally optimal policy, and models sequential tasks with zig-zag diagrams.
- **Why it matters for us.** It is one of the few CT papers that names safety constraints as categorical constructions (pushouts that remove hazards). Its "learning-by-parts = learning-on-whole" conditions are the RL analogue of Will's functoriality tests.

### [RECOMMENDED] `dalrymple2024gsai`
Dalrymple, D. "davidad", Skalse, J., Bengio, Y., Russell, S., Tegmark, M., Seshia, S., Omohundro, S., Szegedy, C., Goldhaber, B., Ammann, N., Abate, A., Halpern, J., Barrett, C., Zhao, D., Zhi-Xuan, T., Wing, J., Tenenbaum, J., 2024. *Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems*. arXiv:2405.06624 (also UC Berkeley EECS-2024-45).  
URL: <https://arxiv.org/abs/2405.06624>  
Topic: guaranteed-safe AI · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2405.06624v3 and https://www2.eecs.berkeley.edu/Pubs/TechRpts/2024/EECS-2024-45.html

- **Summary.** The paper defines "guaranteed safe (GS) AI" as the interplay of three components: a **world model**, a **safety specification** and a **verifier** that yields auditable quantitative guarantees. It surveys how to build each and argues the main alternatives are inadequate.
- **Why it matters for us.** Will's claim-DAG verifier is a small-scale GS-AI pipeline, with the claim DAG as world model, consistency constraints as the spec and budgeted checks as the verifier. This is the paper to cite for that framing.

### [RECOMMENDED] `aria2024safeguarded`
Dalrymple, D. (Programme Director), 2024. *Safeguarded AI: Programme Thesis* (v1). ARIA (Advanced Research + Invention Agency). Companion: *Compositional World Modelling, TA1.1 Theory, Programme Discussion Report*, ARIA, 2024.  
URL: <https://www.aria.org.uk/wp-content/uploads/2024/01/ARIA-Safeguarded-AI-Programme-Thesis-V1.pdf>  
Topic: guaranteed-safe AI --- · Depth read: search snippets only  
Checked against: search results listing both PDFs and https://www.aria.org.uk/programme-safeguarded-ai

- **Summary.** The £59m programme aims to build a "gatekeeper" AI that checks frontier-AI actions against formal world models and probabilistic specs. TA1.1 (Theory) funds the syntax and semantics of languages for world models, specifications and proof certificates, explicitly via category-theoretic algebras of system composition. Per the search results, davidad later moved to Technical Advisor, Nora Ammann became Programme Director, and the programme pivoted toward cybersecurity and microelectronics.
- **Why it matters for us.** This is the main **funded** "CT for AI safety" programme. Its TA1.1 creator list is a map of who is doing categorical safety now. Note the pivot when citing.

### [RECOMMENDED] `christiano2021elk`
Christiano, P., Cotra, A., Xu, M., 2021. *Eliciting Latent Knowledge: How to tell if your eyes deceive you*. ARC technical report (Google Doc; AF/LW post 14 Dec 2021). *(Subtitle from memory; the snippet showed only "Eliciting latent knowledge:".)*  
URL: <https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8>  
Topic: ARC / ELK · Depth read: abstract (search snippets)  
Checked against: search results incl. that doc and https://lesswrong.com/posts/qHCDysDnvhteW7kRd

- **Summary.** A predictor "knows" off-camera facts, such as tampering, that would change our evaluation. ELK asks how to train a reporter that reveals this knowledge and not what a human would believe. The report proceeds as a builder-vs-breaker game of training strategies and counterexamples.
- **Why it matters for us.** The "direct translator vs. human simulator" split is a question about which functor the reporter implements. Consistency tests are one of the few label-free ways to tell them apart.

### [RECOMMENDED] `irving2018debate`
Irving, G., Christiano, P., Amodei, D., 2018. *AI safety via debate*. arXiv:1805.00899.  
URL: <https://arxiv.org/abs/1805.00899>  
Topic: scalable oversight · Depth read: abstract (search snippets)  
Checked against: search results incl. https://www.arxiv.org/abs/1805.00899

- **Summary.** Agents are trained by self-play on a zero-sum debate game judged by a human, so that humans can supervise tasks they cannot judge directly. At equilibrium, debate is argued to be as strong as unrestricted AI. It includes an MNIST sparse-pixel experiment. *(The PSPACE complexity analogy is from memory and was not in the snippets.)*
- **Why it matters for us.** Debate is literally a two-player game whose equilibria certify truth, so it can be stated as an open game. Debate trees are claim DAGs.

### [RECOMMENDED] `christiano2018amplification`
Christiano, P., Shlegeris, B., Amodei, D., 2018. *Supervising strong learners by amplifying weak experts*. arXiv:1810.08575.  
URL: <https://arxiv.org/abs/1810.08575>  
Topic: scalable oversight · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/1810.08575v1

- **Summary.** Iterated Amplification builds a training signal for hard tasks by composing solutions to easier subproblems, similar to Expert Iteration without external reward. Demonstrated on algorithmic tasks.
- **Why it matters for us.** Amplification is decomposition and recomposition, an operad-algebra structure. Whether the distilled model is an algebra homomorphism of the decomposition is exactly a functoriality question.

### [RECOMMENDED] `skalse2022reward`
Skalse, J., Howe, N. H. R., Krasheninnikov, D., Krueger, D., 2022. *Defining and Characterizing Reward Hacking* (NeurIPS 2022 title: *Defining and Characterizing Reward Gaming*). arXiv:2209.13085.  
URL: <https://arxiv.org/abs/2209.13085>  
Topic: reward hacking · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2209.13085v1 and https://proceedings.neurips.cc/paper_files/paper/2022/hash/3d719fee332caa23d5038b8a90e81796-Abstract.html

- **Summary.** A proxy is **unhackable** if increasing expected proxy return can never decrease expected true return. Over all stochastic policies only trivial pairs are unhackable, where one reward is constant. Non-trivial pairs exist for finite or deterministic policy sets. Simplifying a reward by dropping terms or merging distinctions usually does not prevent hacking.
- **Why it matters for us.** **Order-theoretic flavour:** unhackability is a condition between the two preorders that the proxy and true returns induce on policies: whenever J_proxy goes up, J_true must not go down. Reward simplification is a coarsening map on these orders. This is a natural place to state results as monotone maps or Galois connections between policy preorders. The paper states the order-theoretic condition but, as far as the abstract shows, does not use Galois-connection language.

### [RECOMMENDED] `cousot1977abstract`
Cousot, P., Cousot, R., 1977. *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*. POPL '77, pp. 238–252. DOI 10.1145/512950.512973.  
URL: <https://doi.org/10.1145/512950.512973>  
Topic: abstract interpretation · Depth read: abstract (search snippets)  
Checked against: search results incl. https://bibtex.github.io/POPL-1977-CousotC.html and https://cs.nyu.edu/~pmc309/COUSOTpapers/POPL77.shtml

- **Summary.** Program properties are modelled in complete lattices, and abstract interpretations are shown to be consistent with more refined ones. Levels of abstraction themselves form a lattice, and abstract properties are built constructively via fixpoints. *(The explicit Galois-connection (α, γ) formulation is usually credited to Cousot & Cousot 1979; from memory, unverified.)*
- **Why it matters for us.** Galois connections are adjunctions between posets. This is the cleanest bridge from Will's CT toolkit to sound-but-incomplete verification, which is what budgeted verification is.

### [REFERENCE] `hedges2016thesis`
Hedges, J. (Julian), 2016. *Towards compositional game theory*. PhD thesis, Queen Mary University of London.  
URL: <https://qmro.qmul.ac.uk/xmlui/handle/123456789/23259>  
Topic: open games · Depth read: abstract (search snippets)  
Checked against: search result for that QMRO record and its PDF

- **Summary.** The thesis proposes open games as a new foundation for game theory, built algebraically from players and outcome functions. It defines a symmetric monoidal category of open games and shows agreement with classical results for normal-form and some perfect-information games.
- **Why it matters for us.** This is the long-form reference for the definitions if Will needs proofs rather than the LICS summary.

### [REFERENCE] `bolt2019bayesian`
Bolt, J., Hedges, J., Zahn, P., 2023. *Bayesian open games*. Compositionality 5. arXiv:1910.03656.  
URL: <https://arxiv.org/abs/1910.03656>  
Topic: open games · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/1910.03656v2 and https://compositionality.episciences.org/13528

- **Summary.** The paper extends open games to stochastic environments and Bayesian Nash equilibrium, which covers games of incomplete information. It connects open games to lenses, and its proofs use a diagrammatic language for existential lenses.
- **Why it matters for us.** Uncertainty over what an agent knows, an incomplete-information game, is the natural setting for "does the verifier know the model is hallucinating?" questions.

### [REFERENCE] `hedges2024rl`
Hedges, J., Rodríguez Sakamoto, R., 2025. *Reinforcement Learning in Categorical Cybernetics*. EPTCS 429, pp. 270–286. arXiv:2404.02688.  
URL: <https://arxiv.org/abs/2404.02688>  
Topic: categorical cybernetics / RL · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2404.02688v1 and https://strathprints.strath.ac.uk/94389/

- **Summary.** DP, Monte Carlo, TD learning and deep RL are cast as parametrised optics. Bellman operators are lifted to parametrised optics over action-value functions, and a representable contravariant functor then yields Bellman iteration as the backward pass of an agent–environment optic.
- **Why it matters for us.** This is the most direct "lenses for reinforcement learning" reference. It shows how much standard ML fits the optic pattern.

### [REFERENCE] `capucci2022diegetic`
Capucci, M., 2023. *Diegetic representation of feedback in open games*. EPTCS 380 (ACT 2022), pp. 145–158. arXiv:2206.12338.  
URL: <https://arxiv.org/abs/2206.12338>  
Topic: open games · Depth read: abstract (search snippets)  
Checked against: search results incl. https://strathprints.strath.ac.uk/87723 and https://dx.doi.org/10.4204/EPTCS.380.9

- **Summary.** The counterfactual analysis that yields Nash equilibria can be described inside the game's own dynamics, without external equilibrium predicates. The resulting picture nearly coincides with how gradient-based learners are specified and trained.
- **Why it matters for us.** It puts "feedback signals" (rewards, verifier verdicts) inside the compositional structure. That is the right move if verifier feedback is to be a morphism and not an external oracle.

### [REFERENCE] `smithe2021cai`
Smithe, T. St. C., 2021. *Compositional Active Inference I: Bayesian Lenses. Statistical Games*. arXiv:2109.04461.  
URL: <https://arxiv.org/abs/2109.04461>  
Topic: categorical Bayesian inference · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2109.04461v2

- **Summary.** The paper defines Bayesian lenses and proves that Bayesian inversions compose according to the lens pattern. It introduces "statistical games", categories of optimisation objectives for approximate inference, from MLE to variational Bayes.
- **Why it matters for us.** Statistical games attach a *loss* to each lens, so composition carries a cost. This is a ready-made way to talk about where approximation error enters a chain.

### [REFERENCE] `smithe2022thesis`
Smithe, T. St. C., 2023. *Mathematical Foundations for a Compositional Account of the Bayesian Brain*. DPhil thesis, University of Oxford. arXiv:2212.12538.  
URL: <https://arxiv.org/abs/2212.12538>  
Topic: categorical Bayesian inference · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2212.12538 and https://ora.ox.ac.uk/objects/uuid:e5eae609-0306-44fe-97bf-0eabba684983

- **Summary.** The thesis gives the full development of Bayesian lenses and statistical games. It builds functors that describe the bidirectional structure of predictive-coding circuits under the free-energy principle.
- **Why it matters for us.** Book-length reference for the above. Only needed if the project goes deep into the optics machinery.

### [REFERENCE] `libkind2025doubleoperadic`
Libkind, S., Myers, D. J., 2025. *Towards a double operadic theory of systems*. arXiv:2505.18329.  
URL: <https://arxiv.org/abs/2505.18329>  
Topic: categorical systems theory --- · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2505.18329v2

- **Summary.** The paper packages open systems, their interactions and their maps as a symmetric monoidal loose right module over a symmetric monoidal double category. It is the current form of Myers's "categorical systems theory" programme. Myers also leads an ARIA Safeguarded AI TA1.1 project, "Double Categorical Systems Theory for Safeguarded AI", but that detail came from an ARIA/aggregator search snippet and was not checked on an ARIA page.
- **Why it matters for us.** This is the systems-theory side of the CT-for-safety programme that ARIA funds. It is useful to cite, though heavy for an undergrad.

### [REFERENCE] `hubinger2019risks`
Hubinger, E., van Merwijk, C., Mikulik, V., Skalse, J., Garrabrant, S., 2019. *Risks from Learned Optimization in Advanced Machine Learning Systems*. arXiv:1906.01820.  
URL: <https://arxiv.org/abs/1906.01820>  
Topic: agent foundations · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/1906.01820 and https://intelligence.org/2019/06/07/new-paper-learned-optimization/

- **Summary.** The paper introduces *mesa-optimisation*, where a learned model is itself an optimiser whose mesa-objective may differ from the base objective, along with inner alignment and deceptive alignment.
- **Why it matters for us.** Categorically this is a question about whether the "objective" functor commutes with training, i.e. whether the learned agent's objective factors through the specified one. It is a conceptual anchor for "specification vs. learned goal" diagrams.

### [REFERENCE] `langosco2022goal`
Langosco di Langosco, L., Koch, J., Sharkey, L., Pfau, J., Krueger, D., 2022. *Goal Misgeneralization in Deep Reinforcement Learning*. ICML 2022, PMLR 162:12004–12019. arXiv:2105.14111.  
URL: <https://proceedings.mlr.press/v162/langosco22a.html>  
Topic: agent foundations · Depth read: abstract (search snippets)  
Checked against: search results incl. that PMLR page and https://arxiv.org/abs/2105.14111v6. The snippet noted that the arXiv author list additionally includes Laurent Orseau. The ICML author list above matched my query but was not spelled out in full in the snippet.

- **Summary.** RL agents keep their capabilities out of distribution but pursue the wrong goal, for example navigating competently to the wrong place, shown on modified Procgen environments. The actor and critic learn different proxy goals.
- **Why it matters for us.** This is the canonical empirical demonstration that "capability composes, goal does not". It is a structural analogue of a model whose reasoning steps are fluent while its chain is unfaithful.

### [REFERENCE] `shah2022goal`
Shah, R., Varma, V., Kumar, R., Phuong, M., Krakovna, V., Uesato, J., Kenton, Z., 2022. *Goal Misgeneralization: Why Correct Specifications Aren't Enough For Correct Goals*. arXiv:2210.01790.  
URL: <https://arxiv.org/abs/2210.01790>  
Topic: agent foundations --- · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/pdf/2210.01790

- **Summary.** Goal misgeneralisation can occur even with a correct specification: the learned program competently pursues an undesired goal that coincided with good training performance. The paper gives examples across deep learning, including an agent that follows an anti-expert, and argues the catastrophic-risk case.
- **Why it matters for us.** It separates specification error from generalisation error, which is the same separation Will needs between "the claim-DAG spec is wrong" and "the model's composition is wrong".

### [REFERENCE] `davidad2022oaa`
davidad (D. Dalrymple), c. 2022–23 *(exact date unverified)*. *An Open Agency Architecture for Safe Transformative AI*. LessWrong / Alignment Forum post.  
URL: <https://www.lesswrong.com/posts/pKSmEkSQJsCSTK6nH/an-open-agency-architecture-for-safe-transformative-ai>  
Topic: guaranteed-safe AI · Depth read: fragments + secondary summaries  
Checked against: search results incl. https://www.greaterwrong.com/posts/pKSmEkSQJsCSTK6nH/an-open-agency-architecture-for-safe-transformative-ai and the LessWrong OAA tag page. Only fragments of the post were visible.

- **Summary.** The post proposes a strategy built from AI "modellers" that produce descriptive world models and "elicitors" that help humans state desiderata in the world-model's formal language, with policies verified against them. A 2024-03 edit says the draft is largely superseded by the ARIA Safeguarded AI thesis.
- **Why it matters for us.** It is the origin of the "formal world model + formal spec + verification" research agenda that ARIA now funds with explicit category theory.

### [REFERENCE] `christiano2022presumption`
Christiano, P., Neyman, E., Xu, M., 2022. *Formalizing the presumption of independence*. arXiv:2211.06738.  
URL: <https://arxiv.org/abs/2211.06738>  
Topic: ARC / heuristic arguments · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/pdf/2211.06738 and https://stafforini.com/works/christiano-2022-formalizing-presumption-of/

- **Summary.** The paper proposes "heuristic estimators" that formalise defeasible reasoning which presumes independence absent evidence, and lists coherence properties no current candidate satisfies. The open question is whether such an estimator can accept valid heuristic arguments without endorsing spurious ones.
- **Why it matters for us.** The coherence properties of heuristic estimators, such as estimates being stable under adding arguments, are close to monotonicity/Galois-style conditions. They suggest a CT reading of "verification under a budget" as a sequence of refining estimates.

### [REFERENCE] `kenton2024scalable`
Kenton, Z., et al. (11 authors, Google DeepMind), 2024. *On scalable oversight with weak LLMs judging strong LLMs*. NeurIPS 2024. arXiv:2407.04622.  
URL: <https://arxiv.org/abs/2407.04622>  
Topic: scalable oversight · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2407.04622v2 and https://mlanthology.org/neurips/2024/kenton2024neurips-scalable. Only the first author was seen in the snippets, so fill in the full list from arXiv.

- **Summary.** The paper compares debate, consultancy and direct QA with weaker LLM judges over stronger LLM agents, across extractive QA, maths, coding, logic and multimodal tasks. Stronger debaters raise judge accuracy, though more modestly than in prior work.
- **Why it matters for us.** It is the reference empirical protocol for weak-judges-strong. Its open-model variants could be replicated without paid APIs on a smaller scale.

### [REFERENCE] `burns2023w2s`
Burns, C., Izmailov, P., Kirchner, J. H., Baker, B., Gao, L., Aschenbrenner, L., Chen, Y., Ecoffet, A., Joglekar, M., Leike, J., Sutskever, I., Wu, J., 2023. *Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision*. arXiv:2312.09390.  
URL: <https://arxiv.org/abs/2312.09390>  
Topic: scalable oversight · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2312.09390v1

- **Summary.** Strong pretrained models fine-tuned on labels from weaker supervisors often outperform those supervisors. This is offered as an empirical analogy for humans supervising superhuman models. Code is at github.com/openai/weak-to-strong.
- **Why it matters for us.** It gives a cheap, open-model experimental paradigm. Structural constraints such as consistency could be added as an extra "weak supervisor" signal.

### [REFERENCE] `krakovna2020specgaming`
Krakovna, V., Uesato, J., Mikulik, V., Rahtz, M., Everitt, T., Kumar, R., Kenton, Z., Leike, J., Legg, S., 2020. *Specification gaming: the flip side of AI ingenuity*. DeepMind blog, 21 Apr 2020.  
URL: <https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/>  
Topic: specification gaming · Depth read: abstract (search snippets)  
Checked against: search results incl. that page and https://www.lesswrong.com/posts/7b2RJJQ76hjZwarnj/specification-gaming-the-flip-side-of-ai-ingenuity

- **Summary.** The post defines specification gaming as behaviour that satisfies the literal specification of an objective without achieving the intended outcome, and catalogues examples.
- **Why it matters for us.** It is the standard citation for "spec ≠ intent", the gap a Galois connection between intended and specified behaviours is meant to measure.

### [REFERENCE] `pan2022effects`
Pan, A., Bhatia, K., Steinhardt, J., 2022. *The Effects of Reward Misspecification: Mapping and Mitigating Misaligned Models*. ICLR 2022. arXiv:2201.03544.  
URL: <https://arxiv.org/abs/2201.03544>  
Topic: reward hacking --- · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2201.03544v2 and https://mlanthology.org/iclr/2022/pan2022iclr-effects

- **Summary.** Across four RL environments with misspecified rewards, more capable agents (by capacity, action resolution, observation noise, training time) get higher proxy and lower true reward. The authors observe **phase transitions** where true reward drops sharply, and propose anomaly detection for aberrant policies.
- **Why it matters for us.** The phase-transition lens suggests measuring *when* functoriality violations appear as model size grows, a cheap scaling study with open models.

### [REFERENCE] `gehr2018ai2`
Gehr, T., Mirman, M., Drachsler-Cohen, D., Tsankov, P., Chaudhuri, S., Vechev, M., 2018. *AI2: Safety and Robustness Certification of Neural Networks with Abstract Interpretation*. IEEE S&P 2018, pp. 3–18.  
URL: <https://ddana.net.technion.ac.il/files/2019/10/sp18.pdf>  
Topic: abstract interpretation · Depth read: abstract (search snippets)  
Checked against: search results incl. that PDF and https://www.ieee-security.org/TC/SP2018/poster-abstracts/oakland2018-paper50-poster-abstract.pdf

- **Summary.** This is the first sound, scalable abstract-interpretation analyser for realistic NNs, including CNNs. It defines abstract transformers (zonotopes and others) for affine, ReLU and max-pool layers and is much faster than symbolic methods.
- **Why it matters for us.** It shows that compositional (layer-by-layer) sound over-approximation works for NNs. A claim-DAG verifier could propagate abstract truth values the same way.

### [REFERENCE] `singh2019deeppoly`
Singh, G., Gehr, T., Püschel, M., Vechev, M., 2019. *An Abstract Domain for Certifying Neural Networks*. Proc. ACM Program. Lang. 3 (POPL), Article 41. DOI 10.1145/3290354.  
URL: <https://doi.org/10.1145/3290354>  
Topic: abstract interpretation --- · Depth read: abstract (search snippets)  
Checked against: search results incl. https://popl19.sigplan.org/details/POPL-2019-Research-Papers/58/An-Abstract-Domain-for-Certifying-Neural-Networks and https://bibtex.github.io/POPL-2019-SinghGPV.html

- **Summary.** DeepPoly is an abstract domain that combines floating-point polyhedra with intervals, with transformers for affine, ReLU, sigmoid, tanh and maxpool. It is more precise than prior domains, scales to large nets, and with refinement certifies robustness to rotations.
- **Why it matters for us.** It is the standard precision/cost trade-off reference. "Choose a coarser abstract domain to save budget" is the analogue of choosing which claims to verify.

### [REFERENCE] `spera2026noncomp`
Spera, C., 2026. *Safety is Non-Compositional: A Formal Framework for Capability-Based AI Systems*. arXiv:2603.15973.  
URL: <https://arxiv.org/abs/2603.15973>  
Topic: compositional safety --- · Depth read: abstract (search snippets)  
Checked against: search results incl. https://arxiv.org/abs/2603.15973 and https://arxiv.org/html/2603.15973v1

- **Summary.** Agent capabilities are modelled as a hypergraph. With conjunctive capability dependencies, two individually safe agents can jointly reach a forbidden goal via an emergent hyperedge, so safety is not compositional. The paper is not category-theoretic, and it is a single-author industry preprint.
- **Why it matters for us.** It is a clean negative result to state categorically: "safe" is not a sub-operad/sub-monoidal-category closed under composition. Useful as motivation; low authority.


## Cluster F: Empirical LLM compositionality, consistency & uncertainty (the baselines)

### [READ-FIRST] `press2023compositionality`
Press, O., et al. (co-authors not re-verified; see note), 2023. *Measuring and Narrowing the Compositionality Gap in Language Models*. Findings of EMNLP 2023 (search sources disagreed between ICLR 2023 and Findings of EMNLP 2023. Findings of EMNLP 2023 is correct to my knowledge, but it was not confirmed in the proceedings). arXiv:2210.03350 (Oct 2022).  
URL: <https://arxiv.org/abs/2210.03350>  
Topic: compositionality / multi-hop · Depth read: abstract (+ search snippets of figures)  
Checked against: WebSearch listing of arxiv.org/abs/2210.03350, arxiv.org/html/2210.03350v3, and par.nsf.gov/servlets/purl/10533356

- **Summary.** The paper defines the **compositionality gap** as the fraction of 2-hop questions answered wrongly among those whose two sub-questions are both answered correctly. On Compositional Celebrities the gap stays at about **40%** across GPT-3 sizes (davinci 41%; other sizes 38-40%; snippet). Single-hop accuracy grows with scale faster than 2-hop accuracy. Elicitive prompting (chain-of-thought and the proposed **self-ask**) narrows the gap. Reported Bamboogle accuracy on davinci-002 is 57.6% for self-ask against 46.4% for CoT (snippet). A later version reports a gap of 42.9% for ChatGPT and 23.0% for GPT-4, and warns that the GPT-4 figure may be contaminated (snippet).
- **Why it matters for us.** This is **the direct empirical ancestor of delta_comp**. The compositionality gap is a 0/1 version of "F(g∘f) ≠ F(g)∘F(f) even though F(f) and F(g) are correct". delta_comp is its distributional (TV) and label-free version. The survey should state that delta_comp generalises this gap: it needs no gold labels and works on distributions.

### [READ-FIRST] `balesni2024twohop`
Balesni, M., Korbak, T., Evans, O., 2024 (v4 2025). *The Two-Hop Curse: LLMs trained on A->B, B->C fail to learn A->C*. Retitled in v4 (Nov 2025) as *Lessons from Studying Two-Hop Latent Reasoning*. arXiv:2411.16353.  
URL: <https://arxiv.org/abs/2411.16353>  
Topic: compositionality / multi-hop · Depth read: abstract (v1 and v4)  
Checked against: WebSearch listing of arxiv.org/abs/2411.16353v1 (v1 title), arxiv.org/abs/2411.16353v4 (v4 title), and aisi.gov.uk/research/lessons-from-studying-two-hop-latent-reasoning

- **Summary.** The authors fine-tune Llama-3-8B-Instruct and GPT-4o on fictional facts. In v1, models cannot compose two separately learned facts without CoT, and accuracy and test loss fall to chance. They succeed when the facts co-occur in a training document or in the prompt, or when CoT is used. v1 also reports that 9 frontier LLMs fail at no-CoT two-hop for over half of the real-fact question categories. **v4 revises the conclusion**: composition fails when both facts are synthetic but can succeed when one fact is synthetic and the other is natural. The authors now say LLMs are capable of latent two-hop reasoning, with unclear scaling, and warn about "spurious failures" caused by artificial setups.
- **Why it matters for us.** This is a controlled demonstration that the model's "composite morphism" and its "composition of morphisms" can come apart, which is a non-functorial representation. The revision is a caution: **cite v4 and avoid the strong "curse" framing**. Their design (synthetic facts, CoT vs no-CoT) is the natural way to create ground-truth functoriality violations on small models.

### [READ-FIRST] `berglund2024reversal`
Berglund, L., Tong, M., Kaufmann, M., Balesni, M., Stickland, A. C., Korbak, T., Evans, O., 2024. *The Reversal Curse: LLMs trained on "A is B" fail to learn "B is A"*. ICLR 2024.  
URL: <https://arxiv.org/abs/2309.12288>  
Topic: compositionality / inverses · Depth read: abstract  
Checked against: WebSearch listing of proceedings.iclr.cc/paper_files/paper/2024/hash/5178b2f2d7c44aa390c0777dc77b3f0c-Abstract-Conference.html and arxiv.org/abs/2309.12288v1

- **Summary.** GPT-3 and Llama-1 fine-tuned on fictitious "A is B" facts do not generalise to "B is A". The effect holds across model sizes and families and is not fixed by data augmentation. On real celebrity parent questions, GPT-4 answers 79% in the forward direction but 33% in reverse. Given in context, reversal works perfectly, so the failure is specific to what is learned in training.
- **Why it matters for us.** This is the canonical **failure to preserve inverses / the dagger structure (f ↦ f†)**, also readable as failure of the relation-as-span to be symmetric. A "dagger-functoriality" test F(f†) = F(f)† belongs next to Will's composition test as a second categorical law.

### [READ-FIRST] `kassner2021beliefbank`
Kassner, N., Tafjord, O., Schütze, H., Clark, P., 2021. *BeliefBank: Adding Memory to a Pre-Trained Language Model for a Systematic Notion of Belief*. EMNLP 2021 (pp. 8849-8861).  
URL: <https://aclanthology.org/2021.emnlp-main.697/>  
Topic: belief consistency (constraint graphs) · Depth read: abstract (full-text constraint details not reachable)  
Checked against: WebSearch listing of aclanthology.org/2021.emnlp-main.697/ and arxiv.org/abs/2109.14723v1

- **Summary.** A PLM is wrapped in a symbolic memory of beliefs. A **weighted MaxSAT solver** flips beliefs that clash with a graph of implication constraints. A feedback loop re-queries the model with relevant stored beliefs as context. Consistency and accuracy both rise over time in a controlled setting. The paper also releases a constraint dataset (allenai.org/data/beliefbank).
- **Why it matters for us.** This is **global consistency over a graph of beliefs**, the closest prior work to a "sheaf / gluing" reading in which local answers must glue to a consistent global section. delta_comp checks one local law (a composition square). BeliefBank enforces many implication laws together. A categorical survey can present BeliefBank, ConCoRD and Maieutic as "repairing to the nearest functor".

### [READ-FIRST] `fluri2023superhuman`
Fluri, L., Paleka, D., Tramèr, F., 2023. *Evaluating Superhuman Models with Consistency Checks*. arXiv:2306.09983 (also NeurIPS 2023 workshop, per mlanthology; a later archival venue was not confirmed).  
URL: <https://arxiv.org/abs/2306.09983>  
Topic: consistency checks (safety) · Depth read: abstract (+ repo README snippet)  
Checked against: WebSearch listing of arxiv.org/abs/2306.09983v2, mlanthology.org/neuripsw/2023/fluri2023neuripsw-evaluating, and github.com/ethz-privsec/superhuman-ai-consistency

- **Summary.** When ground truth is unavailable, the paper checks logical consistency instead: (1) chess engines (Leela, Stockfish) give different valuations to semantically identical boards; (2) GPT-4 / GPT-3.5 forecasts violate negation, paraphrase, monotonicity (sports records over successive years) and Bayes-rule checks; (3) legal AI, e.g. a bail model that grants bail only after a felony is added to the record.
- **Why it matters for us.** It is the **methodological justification** for delta_comp: label-free consistency checks as a hallucination or error signal when truth is costly. Each check is a categorical law (negation = involution, monotonicity = order-preserving functor, Bayes = compositional structure of conditionals). Will's work extends this to composition of relations.

### [READ-FIRST] `farquhar2024semantic`
Farquhar, S., Kossen, J., Kuhn, L., Gal, Y., 2024. *Detecting hallucinations in large language models using semantic entropy*. Nature 630:625-630.  
URL: <https://doi.org/10.1038/s41586-024-07421-0>  
Topic: uncertainty / hallucination detection · Depth read: abstract (+ secondary-source numbers)  
Checked against: WebSearch listing of pmc.ncbi.nlm.nih.gov/articles/PMC11186750, ora.ox.ac.uk/objects/uuid:0653d09e-..., and oatml.cs.ox.ac.uk/blog/2024/06/19/detecting_hallucinations_2024.html

- **Summary.** Sample several answers, cluster them by **bidirectional entailment** (NLI), and take entropy over the meaning clusters. The method targets "confabulations" (arbitrary, incorrect generations). Secondary sources report an **average AUROC of about 0.79 against about 0.69 for the best baseline**, over 30 task × model combinations (TriviaQA, SQuAD, BioASQ, NQ-Open, SVAMP, FactualBio; LLaMA-2-Chat, Falcon, Mistral). Baselines include naive entropy, P(True) and embedding regression. **Verify exact numbers in the paper.** Cost is about 10× a single generation.
- **Why it matters for us.** **The main baseline.** delta_comp is computed over answer distributions, so it should use the same semantic clustering (compare clustered distributions, not strings). The key question is whether delta_comp adds AUROC over semantic entropy. Categorically, semantic clustering is a quotient by an equivalence relation, i.e. evaluation in the category whose objects are meanings rather than strings.

### [RECOMMENDED] `dziri2023faith`
Dziri, N., Lu, X., Sclar, M., Li, X. L., Jiang, L., Lin, B. Y., West, P., Bhagavatula, C., Le Bras, R., Hwang, J. D., Sanyal, S., Welleck, S., Ren, X., Ettinger, A., Harchaoui, Z., Choi, Y., 2023. *Faith and Fate: Limits of Transformers on Compositionality*. NeurIPS 2023.  
URL: <https://arxiv.org/abs/2305.18654>  
Topic: compositionality / multi-hop · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2305.18654v3 and nips.cc/virtual/2023/poster/72247

- **Summary.** The paper models compositional tasks (multi-digit multiplication, logic grid puzzles, dynamic programming) as computation graphs. It argues that transformers solve them by "linearized subgraph matching", i.e. pattern-matching fragments seen in training, rather than systematic composition. Errors compound with graph depth.
- **Why it matters for us.** It gives a computation-graph and DAG framing of composition that sits naturally beside a categorical one. It also predicts that functoriality violations grow with chain length, which explains why Will's signal weakens beyond 2 hops: everything is wrong by then.

### [RECOMMENDED] `allenzhu2025physics32`
Allen-Zhu, Z., Li, Y., 2025. *Physics of Language Models: Part 3.2, Knowledge Manipulation*. ICLR 2025 (arXiv:2309.14402, 2023).  
URL: <https://arxiv.org/abs/2309.14402>  
Topic: compositionality / inverses · Depth read: abstract  
Checked against: WebSearch listing of proceedings.iclr.cc/paper_files/paper/2025/hash/d5494c8747276d3cdb2598e5617de89d-Abstract-Conference.html

- **Summary.** In controlled synthetic biography data, models retrieve stored attributes well but struggle with classification and comparison unless CoT is used in both training and inference. **Inverse search** ("which person has attribute T?") is essentially 0% whatever the prompt. The authors argue the findings extend to GPT-4.
- **Why it matters for us.** It is a cleaner, synthetic analogue of the reversal curse, with a controlled pretraining set. It is also a template for small-model experiments where functoriality and inverse laws can be checked against known ground truth.

### [RECOMMENDED] `zhong2023mquake`
Zhong, Z., Wu, Z., Manning, C. D., Potts, C., Chen, D., 2023. *MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions*. EMNLP 2023 (pp. 15686-15702).  
URL: <https://aclanthology.org/2023.emnlp-main.971>  
Topic: compositionality / editing · Depth read: title/authors/venue (content from memory: knowledge edits typically do not propagate to multi-hop questions that depend on the edited fact. Confirm in the paper.)  
Checked against: WebSearch listing of aclanthology.org/2023.emnlp-main.971 and arxiv.org/abs/2305.14795v3

- **Summary.** The benchmark checks whether editing a single fact (f ↦ f') propagates to multi-hop questions that compose the edited fact.
- **Why it matters for us.** Knowledge editing as **naturality**. After an edit, F(g∘f') should equal F(g)∘F(f'). MQuAKE is a ready dataset of chains where functoriality should hold after an intervention.

### [RECOMMENDED] `elazar2021pararel`
Elazar, Y., Kassner, N., Ravfogel, S., Ravichander, A., Hovy, E., Schütze, H., Goldberg, Y., 2021. *Measuring and Improving Consistency in Pretrained Language Models*. TACL 9:1012-1031.  
URL: <https://doi.org/10.1162/tacl_a_00410>  
Topic: consistency benchmarks · Depth read: abstract  
Checked against: WebSearch listing of transacl.org/ojs/index.php/tacl/article/view/3015 and arxiv.org/abs/2102.01017v2

- **Summary.** ParaRel is a set of cloze paraphrases of factual relations. PLMs are poorly consistent across paraphrases. The paper proposes a consistency loss to improve this.
- **Why it matters for us.** Paraphrase invariance is the "identity / isomorphism" law: semantically equal queries should map to equal outputs, i.e. F is well defined on isomorphism classes. Will should report paraphrase consistency as a baseline next to delta_comp.

### [RECOMMENDED] `jang2022becel`
Jang, M., Kwon, D. S., Lukasiewicz, T., 2022. *BECEL: Benchmark for Consistency Evaluation of Language Models*. COLING 2022 (pp. 3680-3696).  
URL: <https://aclanthology.org/2022.coling-1.324/>  
Topic: consistency benchmarks · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2022.coling-1.324/ and cs.ox.ac.uk/publications/publication14945-abstract.html

- **Summary.** The paper defines LM consistency behaviourally and gives a taxonomy (semantic, negational, symmetric, transitive, additive). The benchmark has 19 test cases over 7 downstream tasks. No PLM does well on all of them, and larger models are not necessarily more consistent.
- **Why it matters for us.** Its taxonomy maps closely onto categorical laws: symmetric ↔ dagger, transitive ↔ composition, negational ↔ complement or involution. A useful table for the survey.

### [RECOMMENDED] `mitchell2022concord`
Mitchell, E., Noh, J. J., Li, S., Armstrong, W. S., Agarwal, A., Liu, P., Finn, C., Manning, C. D., 2022. *Enhancing Self-Consistency and Performance of Pre-Trained Language Models through Natural Language Inference*. EMNLP 2022 (pp. 1754-1768).  
URL: <https://arxiv.org/abs/2211.11875>  
Topic: belief consistency (constraint graphs) · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2211.11875v1 and preview.aclanthology.org/setup/2022.emnlp-main.115

- **Summary.** ConCoRD samples candidate answers and builds a factor graph that combines base-model confidences with pairwise NLI relations (entailment and contradiction) from an off-the-shelf NLI model. Weighted MaxSAT then picks jointly consistent answers, with no fine-tuning. It improves accuracy and consistency on closed-book QA and VQA, e.g. +5% absolute for LXMERT on ConVQA.
- **Why it matters for us.** It is a strong **repair baseline**. If delta_comp flags a chain, the natural next step is ConCoRD-style joint inference over {direct answer, hop-1 answer, hop-2 answer}. The NLI-based relation graph also matches the Kuhn/Farquhar clustering.

### [RECOMMENDED] `paleka2025forecasters`
Paleka, D., et al., 2025. *Consistency Checks for Language Model Forecasters*. ICLR 2025 (oral). arXiv:2412.18544.  
URL: <https://arxiv.org/abs/2412.18544>  
Topic: consistency checks (safety) · Depth read: abstract (+ intro snippet)  
Checked against: WebSearch listing of proceedings.iclr.cc/paper_files/paper/2025/file/5107a33432b9a5cffafd0a53ef6c6a18-Paper-Conference.pdf and iclr.cc/virtual/2025/poster/28220 (full co-author list not captured)

- **Summary.** Defines an **arbitrage metric**: the minimum profit an arbitrageur is guaranteed by betting against a forecaster's logically inconsistent probabilities. An automated pipeline generates linked checks, and a benchmark of about 3,000 checks resolves in 2028. Consistency metrics correlate with later Brier scores. Training against a set of checks ("ArbitrageForecaster") does **not** generalise to held-out checks or improve accuracy.
- **Why it matters for us.** The arbitrage metric is a principled, decision-theoretic **alternative to TV distance** for scoring a violated commuting square. The correlation with Brier scores is the analogue of "delta_comp predicts errors". The non-generalisation result warns against optimising directly for functoriality.

### [RECOMMENDED] `ghosh2025logical`
Ghosh, B., Hasan, S., Arafat, N. A., Khan, A., 2025. *Logical Consistency of Large Language Models in Fact-Checking*. ICLR 2025.  
URL: <https://arxiv.org/abs/2412.16100>  
Topic: logical consistency · Depth read: abstract  
Checked against: WebSearch listing of proceedings.iclr.cc/paper_files/paper/2025/hash/3209cf3312b2cbb68e33644362ddc2bd-Abstract-Conference.html and arxiv.org/abs/2412.16100v2

- **Summary.** Builds three KG-grounded logical fact-checking datasets (FreebaseLFC, NELLLFC, WikiLFC). Defines consistency measures for propositional queries (negation, conjunction, disjunction). LLMs are inconsistent, especially on complex queries. Supervised fine-tuning gives about 14% average improvement.
- **Why it matters for us.** Consistency under **logical connectives**, the Boolean-algebra or lattice-homomorphism laws, which complements composition of relations. It is KG-grounded, as MuSiQue-derived chains are.

### [RECOMMENDED] `mundler2024selfcontradictory`
Mündler, N., He, J., Jenko, S., Vechev, M., 2024. *Self-contradictory Hallucinations of Large Language Models: Evaluation, Detection and Mitigation*. ICLR 2024.  
URL: <https://arxiv.org/abs/2305.15852>  
Topic: consistency-based hallucination detection · Depth read: abstract  
Checked against: WebSearch listing of proceedings.iclr.cc/paper_files/paper/2024/hash/b0d4b9d3dc41b36cad1d36ddd27858ab-Abstract-Conference.html and arxiv.org/abs/2305.15852

- **Summary.** 17.7% of ChatGPT sentences contain self-contradictions. A prompting-based detector reaches about 80% F1, and an iterative mitigation removes contradictions. About 35% of contradictions cannot be checked against Wikipedia.
- **Why it matters for us.** Black-box, label-free contradiction detection. It is a close behavioural cousin of delta_comp, applied to free text rather than chains.

### [RECOMMENDED] `li2024drowzee`
Li, N., Li, Y., Liu, Y., Shi, L., Wang, K., Wang, H., 2024. *Drowzee: Metamorphic Testing for Fact-Conflicting Hallucination Detection in Large Language Models*. Proc. ACM Program. Lang. 8(OOPSLA2), Article 336 (OOPSLA 2024).  
URL: <https://arxiv.org/abs/2405.00648>  
Topic: metamorphic testing · Depth read: abstract  
Checked against: WebSearch listing of 2024.splashcon.org/details/splash-2024-oopsla/119/... and arxiv.org/html/2405.00648v2

- **Summary.** Starts from Wikipedia triples and uses Prolog reasoning rules (including **composition** and negation) to generate new questions with derived ground truth automatically. The LLM's answer and reasoning are parsed into a semantic graph and compared with the ground truth. Hallucination rates of 24.7%-59.8% across six LLMs.
- **Why it matters for us.** **Metamorphic testing is functoriality testing by another name.** The composition rule here is the categorical composition law, with a symbolic oracle. It is the closest software-engineering prior work and must be cited as such.

### [RECOMMENDED] `kuhn2023semantic`
Kuhn, L., Gal, Y., Farquhar, S., 2023. *Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation*. ICLR 2023 (notable top 25%).  
URL: <https://arxiv.org/abs/2302.09664>  
Topic: uncertainty · Depth read: abstract  
Checked against: WebSearch listing of iclr.cc/virtual/2023/poster/11013 and mlanthology.org/iclr/2023/kuhn2023iclr-semantic

- **Summary.** Introduces semantic entropy, computed with NLI bidirectional-entailment clustering. It predicts QA accuracy better than comparable baselines, is unsupervised, and needs no change to the model.
- **Why it matters for us.** The original method. Cite it alongside Farquhar 2024.

### [RECOMMENDED] `manakul2023selfcheckgpt`
Manakul, P., Liusie, A., Gales, M. J. F., 2023. *SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models*. EMNLP 2023 (pp. 9004-9017).  
URL: <https://aclanthology.org/2023.emnlp-main.557>  
Topic: consistency-based hallucination detection · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2023.emnlp-main.557 and arxiv.org/abs/2303.08896

- **Summary.** Sample several responses. Facts that are not supported across the samples are flagged as hallucinated. Black-box (no logits). Better sentence-level AUC-PR than grey-box baselines on WikiBio GPT-3 passages.
- **Why it matters for us.** The standard black-box sampling-consistency baseline, and essentially Will's "self-consistency" baseline.

### [RECOMMENDED] `wang2023selfconsistency`
Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., Zhou, D., 2023. *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR 2023.  
URL: <https://arxiv.org/abs/2203.11171>  
Topic: uncertainty / self-consistency · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2203.11171 and mlanthology.org/iclr/2023/wang2023iclr-selfconsistency

- **Summary.** Sample diverse CoT paths and majority-vote the final answer. Gains: GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2%, StrategyQA +6.4%, ARC-c +3.9% (PaLM-540B / GPT-3).
- **Why it matters for us.** Defines the self-consistency (majority-agreement) confidence that, at scale, matched delta_comp's predictive power in Will's results.

### [RECOMMENDED] `kadavath2022know`
Kadavath, S., et al. (Anthropic; Kaplan, J. is last author; full list not re-verified), 2022. *Language Models (Mostly) Know What They Know*. arXiv:2207.05221.  
URL: <https://arxiv.org/abs/2207.05221>  
Topic: uncertainty / calibration · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2207.05221v1 and anthropic.com/research/language-models-mostly-know-what-they-know

- **Summary.** Large models are well calibrated on multiple-choice and true/false questions in the right format. **P(True)** is self-evaluation of a proposed answer and improves when the model sees several of its own samples. **P(IK)**, the probability "I know" the answer, is learnable and partly generalises across tasks, but its calibration transfers poorly.
- **Why it matters for us.** The P(True) and P(IK) baselines. Also shows that calibration emerges with scale, which may explain why delta_comp adds little beyond confidence for large models.

### [RECOMMENDED] `trivedi2022musique`
Trivedi, H., Balasubramanian, N., Khot, T., Sabharwal, A., 2022. *MuSiQue: Multihop Questions via Single-hop Question Composition*. TACL 10:539-554.  
URL: <https://aclanthology.org/2022.tacl-1.31>  
Topic: datasets · Depth read: abstract  
Checked against: WebSearch listing of aclweb.org/anthology/2022.tacl-1.31.pdf and arxiv.org/abs/2108.00573v3

- **Summary.** Built bottom-up by composing connected single-hop questions, where one hop needs the other's answer. 25K questions of 2-4 hops. 3× larger human-machine gap than earlier datasets, and a 30-point F1 drop for single-hop "cheating" models. MuSiQue-Full adds unanswerable contrast questions (a further 14 F1 drop).
- **Why it matters for us.** **Will's dataset.** Its construction is literally composition of morphisms, and its decompositions give the f and g needed for the functoriality test.

### [REFERENCE] `jung2022maieutic`
Jung, J., Qin, L., Welleck, S., Brahman, F., Bhagavatula, C., Le Bras, R., Choi, Y., 2022. *Maieutic Prompting: Logically Consistent Reasoning with Recursive Explanations*. EMNLP 2022 (pp. 1266-1279).  
URL: <https://aclanthology.org/2022.emnlp-main.82>  
Topic: belief consistency (constraint graphs) · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2205.11822 and preview.aclanthology.org/setup/2022.emnlp-main.82

- **Summary.** The model recursively generates abductive explanations for both True and False into a tree. Weighted MAX-SAT over the explanations' logical relations then infers truth values. Accuracy is up to 20% better than prior prompting methods on true/false QA.
- **Why it matters for us.** Another "global section over a diagram" method. The tree of propositions is a small diagram whose consistent assignment acts as a limit or cone.

### [REFERENCE] `hase2023beliefs`
Hase, P., Diab, M., Celikyilmaz, A., Li, X., Kozareva, Z., Stoyanov, V., Bansal, M., Iyer, S., 2023. *Methods for Measuring, Updating, and Visualizing Factual Beliefs in Language Models*. EACL 2023 (pp. 2714-2731).  
URL: <https://aclanthology.org/2023.eacl-main.199>  
Topic: belief consistency · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2023.eacl-main.199 and arxiv.org/pdf/2111.13654

- **Summary.** Proposes logical-consistency metrics for belief updates, the SLAG update objective, and **belief graphs**, built by editing each belief and recording which other beliefs change. Models are only partly consistent.
- **Why it matters for us.** Belief graphs give an empirical dependency structure, a kind of "nerve" of the model's knowledge, to set against the ideal composition structure.

### [REFERENCE] `kassner2020negated`
Kassner, N., Schütze, H., 2020. *Negated and Misprimed Probes for Pretrained Language Models: Birds Can Talk, But Cannot Fly*. ACL 2020 (pp. 7811-7818).  
URL: <https://aclanthology.org/2020.acl-main.698>  
Topic: negation · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2020.acl-main.698 and arxiv.org/abs/1911.03343

- **Summary.** Negated LAMA: PLMs complete "Birds cannot [MASK]" much as they complete the affirmative. Mispriming (prepending a distractor) easily misleads them.
- **Why it matters for us.** Shows that negation as an involution (¬¬ = id; F(¬p) = ¬F(p)) is not respected. Also a cheap test that runs on small masked and causal LMs.

### [REFERENCE] `ravichander2022condaqa`
Ravichander, A., Gardner, M., Marasović, A., 2022. *CONDAQA: A Contrastive Reading Comprehension Dataset for Reasoning about Negation*. EMNLP 2022 (pp. 8729-8755).  
URL: <https://aclanthology.org/2022.emnlp-main.598>  
Topic: negation · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2022.emnlp-main.598 and arxiv.org/abs/2211.00295v1

- **Summary.** 14,182 QA pairs with over 200 negation cues, built as contrastive edits of passages.
- **Why it matters for us.** A dataset for negation-invariance or negation-equivariance tests.

### [REFERENCE] `kossen2024sep`
Kossen, J., Han, J., Razzak, M., Schut, L., Malik, S., Gal, Y., 2024. *Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs*. arXiv:2406.15927 (ICML 2024 workshop).  
URL: <https://arxiv.org/abs/2406.15927>  
Topic: uncertainty (white-box) · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2406.15927 and oatml.cs.ox.ac.uk/publications/20240621_KossenSemantic.html

- **Summary.** Linear probes on hidden states, trained to predict semantic entropy, so only one generation is needed at test time. They generalise better than accuracy probes but trail the full sampling methods.
- **Why it matters for us.** Suggests a "functoriality probe": predict delta_comp from hidden states of the direct query alone. This is feasible on small models.

### [REFERENCE] `xiong2024verbalized`
Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B., 2024. *Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs*. ICLR 2024.  
URL: <https://arxiv.org/abs/2306.13063>  
Topic: uncertainty / calibration · Depth read: title/authors/venue (content from memory: verbalised confidences are overconfident, and sampling plus aggregation strategies help. Confirm in the paper.)  
Checked against: WebSearch listing of iclr.cc/virtual/2024/poster/18135 and arxiv.org/abs/2306.13063

- **Summary.** A systematic evaluation of black-box confidence elicitation: verbalised confidence, sampling consistency, and their combinations.
- **Why it matters for us.** Supplies the verbalised-confidence baseline for black-box API models.

### [REFERENCE] `dhuliawala2024cove`
Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., Weston, J., 2024. *Chain-of-Verification Reduces Hallucination in Large Language Models*. Findings of ACL 2024 (pp. 3563-3578).  
URL: <https://aclanthology.org/2024.findings-acl.212>  
Topic: mitigation · Depth read: title/authors/venue (method from memory: draft an answer, plan verification questions, answer them independently, then revise.)  
Checked against: WebSearch listing of aclanthology.org/2024.findings-acl.212 and bohrium.dp.tech/paper/arxiv/2309.11495

- **Summary.** A draft answer is verified by answering decomposed verification questions independently, then the answer is revised.
- **Why it matters for us.** An operational "decompose and check" loop, and the natural mitigation once delta_comp flags a chain. Comparing direct and stepwise answers is a minimal CoVe.

### [REFERENCE] `song2025halludet`
Song, Y., Qiu, L., Zhang, X., Tang, Z., 2025. *Hallucination Detection via Internal States and Structured Reasoning Consistency in Large Language Models*. arXiv:2510.11529.  
URL: <https://arxiv.org/abs/2510.11529>  
Topic: consistency-based hallucination detection (recent) · Depth read: abstract  
Checked against: WebSearch listing of arxiv.org/abs/2510.11529v2

- **Summary.** Combines internal-state probing (good on factual errors) with CoT-reasoning consistency checks (good on logical errors), and beats either alone on 3 benchmarks with 2 LLMs.
- **Why it matters for us.** Recent evidence that consistency signals and white-box uncertainty are **complementary**. This supports reporting delta_comp's incremental value in a combined detector rather than alone.

### [REFERENCE] `lin2022truthfulqa`
Lin, S., Hilton, J., Evans, O., 2022. *TruthfulQA: Measuring How Models Mimic Human Falsehoods*. ACL 2022 (pp. 3214-3252).  
URL: <https://aclanthology.org/2022.acl-long.229>  
Topic: truthfulness · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2022.acl-long.229 and arxiv.org/abs/2109.07958

- **Summary.** 817 questions in 38 categories. The best model was truthful on 58% against 94% for humans. Larger models were often less truthful ("imitative falsehoods").
- **Why it matters for us.** A contrast case. Imitative falsehoods can be perfectly **consistent**, i.e. functorial but wrong. Consistency checks cannot detect a coherent but false model of the world, and the survey should say this.

### [REFERENCE] `ho2020twowiki`
Ho, X., Duong Nguyen, A.-K., Sugawara, S., Aizawa, A., 2020. *Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps*. COLING 2020 (pp. 6609-6625).  
URL: <https://aclanthology.org/2020.coling-main.580>  
Topic: datasets · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/2020.coling-main.580 and arxiv.org/abs/2011.01060v1

- **Summary.** 2WikiMultiHopQA combines Wikidata triples with Wikipedia text and gives an evidence path (a triple chain) for each question.
- **Why it matters for us.** The evidence triples give **explicit, typed relation chains** (r1∘r2), well suited to per-relation functoriality analysis and to replicating the MuSiQue results.

### [REFERENCE] `yang2018hotpotqa`
Yang, Z., Qi, P., Zhang, S., Bengio, Y., Cohen, W. W., Salakhutdinov, R., Manning, C. D., 2018. *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. EMNLP 2018 (pp. 2369-2380).  
URL: <https://aclanthology.org/D18-1259/>  
Topic: datasets --- · Depth read: abstract  
Checked against: WebSearch listing of aclanthology.org/D18-1259/ and arxiv.org/abs/1809.09600v1

- **Summary.** 113k Wikipedia QA pairs, with sentence-level supporting facts and comparison questions.
- **Why it matters for us.** The standard dataset, but many of its questions can be shortcut (see MuSiQue and 2Wiki). Use it only as a secondary benchmark.
