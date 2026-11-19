# 05 — Category theory primer (only what this survey uses)

[← back to README](README.md)

Each concept gets: a one-paragraph definition, **an ML/safety example tied to this repo**, and **where to learn it**. The four textbooks below are standard and free or cheap:

| Short name | Book | Why |
|---|---|---|
| **7S** | Brendan Fong & David I. Spivak, *An Invitation to Applied Category Theory: Seven Sketches in Compositionality* (Cambridge UP, 2019; free draft at arXiv:1803.05316) | Most applied; Galois connections, enrichment, operads, sheaves, all with examples. Start here. |
| **Leinster** | Tom Leinster, *Basic Category Theory* (Cambridge UP, 2014; free at arXiv:1612.09375) | Short and rigorous: functors, natural transformations, adjunctions, Yoneda, limits. |
| **Riehl** | Emily Riehl, *Category Theory in Context* (Dover, 2016; free PDF on the author's site) | Deeper; Kan extensions ("all concepts are Kan extensions"). |
| **nLab** | <https://ncatlab.org> | Reference wiki. Terse but authoritative. |

Specialised sources are in [01_literature_map.md](01_literature_map.md); keys like `fritz2020synthetic` refer to entries there.

> Reading tip: you do not need the whole of any book. For this survey, 7S chapters 1–4 and 7 plus Leinster chapters 1–4 cover nearly everything below. Markov categories and sheaf Laplacians come from papers, not textbooks.

---

## 1. Category, functor, composition

A **category** has objects, morphisms `f : A → B`, identities and an associative composition `g ∘ f`. A **functor** `F : C → D` sends objects to objects and morphisms to morphisms, preserving identities and composition: `F(g ∘ f) = F(g) ∘ F(f)`.

* **Example (Will's project).** The *task category* has types (Person, Company, Country) as objects and relations (founded, headquartered-in) as morphisms. A perfectly reliable QA system would be a functor into answers. `delta_comp` measures how far `F(g ∘ f)(x) = F(g)(F(f)(x))` fails. **Caveat:** natural-language relations are partial and many-valued, so the target is really the category of *Markov kernels* (§9), not functions.
* **Safety reading.** A "law" a trustworthy system should satisfy, checkable without knowing the right answer.
* **Learn:** Leinster ch. 1; 7S ch. 3.

## 2. Free category on a graph; paths and diagrams

Given a directed graph, the **free category** has the vertices as objects and the *paths* as morphisms. A **diagram** is a functor from a small (often free) category. A diagram **commutes** if all parallel paths agree.

* **Example.** A MuSiQue decomposition (or a claim DAG from `dag_codes/`) generates a free category; "two routes to the same answer must agree" is "this diagram commutes". Overlapping regions in Will's 3–4 hop chains are sub-diagrams.
* **Learn:** 7S ch. 3.1–3.3.

## 3. Natural transformation, naturality square

Given functors `F, G : C → D`, a **natural transformation** `η : F ⇒ G` gives a component `η_A : F(A) → G(A)` per object such that `G(f) ∘ η_A = η_B ∘ F(f)` for every `f : A → B` (the naturality square commutes).

* **Examples.** (i) *Paraphrase/translation*: `F` = "answer in English", `G` = "answer in French", `η` = translation. Naturality says translate-then-answer = answer-then-translate. A failing square is a consistency violation (cf. ParaRel `elazar2021pararel`, metamorphic testing `yang2025metaqa`). (ii) *Model stitching*: an affine map `T` between two models' layers is "natural" if it commutes with every relation map (`bansal2021revisiting`, `hernandez2024linearity`). (iii) *Causal abstraction*: Otsuka & Saigo (`otsuka2022equivalence`) phrase abstraction as a natural transformation; interchange-intervention accuracy (`geiger2025causal`) measures how far its square commutes.
* **Learn:** Leinster ch. 1.3; 7S ch. 3.3.

## 4. Duals, inverses, dagger categories

An **isomorphism** has a two-sided inverse. A **dagger category** has an involution `f ↦ f†` (`(g∘f)† = f†∘g†`) generalising the relational converse.

* **Example.** The *reversal curse* (`berglund2024reversal`): a model that learns `A is-parent-of B` does not answer `B is-child-of A`. Read categorically, the model's "functor" fails to preserve the dagger (relational converse). Our pilot B shows the effect in a tiny transformer.
* **Learn:** nLab "dagger category"; 7S ch. 2 (relations).

## 5. Galois connections and adjunctions

A **Galois connection** between posets is a pair of monotone maps `L ⊣ R` with `L(a) ≤ b ⇔ a ≤ R(b)`. An **adjunction** is the categorical generalisation.

* **Examples.** (i) *Abstract interpretation* (`cousot1977abstract`, `gehr2018ai2`, `singh2019deeppoly`): concrete sets of states and abstract domains (intervals, polyhedra) form a Galois connection. Sound neural-network verification is built on it. (ii) *Specification vs behaviour*: "the strongest spec this policy satisfies" and "the set of policies satisfying this spec" form a Galois connection. Reward-hacking results (`skalse2022reward`) are order-theoretic statements about proxy and true reward orderings. This is speculative but a natural formalism. (iii) *Verification budgets*: coarse abstract truth values propagated through a claim DAG, refined only where too coarse.
* **Learn:** 7S ch. 1.4 (Galois connections, very gentle); Leinster ch. 2 (adjunctions).

## 6. Yoneda lemma ("an object is known by its relationships")

For a locally small category, an object `A` is determined up to isomorphism by the functor `Hom(−, A)` (or `Hom(A, −)`), i.e. by how everything maps into (out of) it.

* **Example.** Bradley, Terilla & Vlassopoulos (`bradley2022enriched`) model meaning of a text as the [0,1]-enriched copresheaf of its continuation probabilities. Safety use: a *fabricated* entity should have an incoherent "relationship profile" compared with a real one. This motivates "Yoneda probes" that query an entity through many relations and score the coherence of the answers.
* **Learn:** Leinster ch. 4; 7S ch. 2.5 for the enriched version.

## 7. Limits, colimits, pullbacks, pushouts

A **limit** of a diagram is the universal object that maps consistently into all of it (products, pullbacks, equalisers). **Colimits** are dual (coproducts, pushouts, gluing).

* **Examples.** "Glue local answers into one consistent world" is a limit (the set of global sections of a sheaf is a limit). Combining sub-agents or MDPs along shared interfaces is a pushout (Bakirtzis et al., `bakirtzis2022mdp`, use pushouts in a category of MDPs to "puncture" hazards).
* **Learn:** Leinster ch. 5; 7S ch. 3.5.

## 8. Monoidal categories and string diagrams

A **monoidal category** has a tensor `⊗` for parallel composition. **String diagrams** are its graphical calculus, and equal diagrams denote equal morphisms.

* **Example.** Reasoning pipelines, tool calls and agents compose both in sequence (`∘`) and in parallel (`⊗`). String diagrams are the lingua franca of open games, Markov categories and DisCoCat. Safety question: which properties are preserved by `∘` and `⊗`? Spera (`spera2026noncomp`) argues safety is not.
* **Learn:** 7S ch. 4 (resource theories, wiring diagrams); Piedeleu & Zanasi, "An Introduction to String Diagrams for Computer Scientists" (a standard tutorial; not otherwise cited or verified here).

## 9. Markov categories (categorical probability)

A **Markov category** is a symmetric monoidal category in which every object can be copied and deleted. Its morphisms behave like stochastic maps. The main example is **Stoch** / the Kleisli category of the distribution monad: morphisms are Markov kernels `P(y | x)`, and composition is the Chapman–Kolmogorov sum `(g ∘ f)(z | x) = Σ_y g(z | y) f(y | x)`. **Deterministic** morphisms are those that commute with copying (`fritz2020synthetic`). Conditional independence, sufficient statistics, de Finetti and d-separation all have synthetic versions.

* **Example (central to this survey).** Each LLM "hop" is a kernel. The *right* stepwise distribution is the Kleisli composite `Σ_y P(z | y, g) P(y | x, f)`, not "plug in the argmax `y`". Then `delta_comp = TV(P_direct, Kleisli composite)` is exactly a composition defect in Stoch. Pilot B computes this exactly. Perrone's entropy (`perrone2024markov`) measures distance from determinism, a categorical cousin of semantic entropy.
* **Learn:** Fritz 2020 (`fritz2020synthetic`) §1–4; Perrone, *Starting Category Theory* / categorical-probability lecture notes (nLab "Markov category" links them).

## 10. Enriched and metric categories

A category **enriched** in `([0,∞], ≥, +)` (a *Lawvere metric space*) has a distance instead of a hom-set. Enrichment in `[0,1]` gives probabilities.

* **Example.** If answer-distributions live in a metric space (TV, KL, Wasserstein), "functor up to ε" becomes a lax or metric functor with a **functoriality defect**. The triangle inequality then gives a testable bound: the defect of a long chain is at most the sum of the defects of its pieces (cf. Rischel & Weichwald's compositional abstraction error, `rischel2021compositional`). This is the principled way to aggregate Will's region scores; the paper found that `max` over regions saturates.
* **Learn:** 7S ch. 2 (enriched categories, Lawvere metric spaces); `bradley2022enriched`.

## 11. Lenses, optics, Para

A **lens** `(get, put)` pairs a forward map with a backward update. **Optics** generalise lenses. **Para** adds parameters. Gradient-based learning (`cruttwell2022categorical`, `fong2019backprop`), Bayesian inversion (`smithe2020bayesian`, "Bayesian updates compose optically") and value iteration (`hedges2022value`) are lens composition.

* **Example.** A two-hop chain as composed Bayesian lenses: forward = answer, backward = "given the answer is wrong, which hop is to blame?" (blame attribution for a verifier). RLHF/reward modelling as a lens: forward = policy acts, backward = reward signal updates. Reward hacking is a failure of the backward pass to track the true objective. Pure framing so far.
* **Learn:** `capucci2021foundations` (categorical cybernetics); Gavranović's thesis (`gavranovic2024fundamental`).

## 12. Operads

An **operad** has operations with many inputs and one output, plus a substitution rule. An **algebra** of an operad interprets each operation. Operads model hierarchical composition (wiring diagrams, task decomposition).

* **Example (important!).** Bottman & Richardson (`bottman2026operads`) model question decomposition as a "questions operad" and QA systems as its algebras. Their "operadic consistency" (`bottman2026operadic`) is the same direct-vs-decomposed test Will runs, so it is the closest prior art. Tool-using agents also compose operadically.
* **Learn:** 7S ch. 6 (operads, wiring diagrams); nLab "operad".

## 13. Sheaves on graphs, cohomology, sheaf Laplacians

A **cellular sheaf** `F` on a graph assigns a vector space (*stalk*) `F(v)` to each vertex and `F(e)` to each edge, and a linear *restriction map* `F_{v⊴e} : F(v) → F(e)` for each incident pair. A **0-cochain** `x` picks a vector per vertex. The **coboundary** is `(δx)_e = F_{v⊴e} x_v − F_{u⊴e} x_u` for `e = (u,v)`. **Global sections** `H^0 = ker δ` are perfectly consistent assignments. `H^1 = coker δ` measures obstructions to fixing edge data (it needs cycles). The **sheaf Laplacian** is `L_F = δᵀδ`, and `xᵀ L_F x = Σ_e ||(δx)_e||²` is the *Dirichlet energy* (total inconsistency) (`hansen2019spectral`). Robinson's **consistency radius** (`robinson2020assignments`) is the metric (non-linear) version.

* **Example.** Each claim in a reasoning DAG is a vertex, and each dependency is an edge whose restriction maps encode what one claim implies about another. A high-energy edge marks a place where local answers fail to glue. Pilot A implements this on `dag_codes` DAGs. Abramsky–Brandenburger contextuality (`abramsky2011sheaf`) is the stronger case where every local pair agrees yet no global section exists. Separating "local disagreement" (signalling) from "global obstruction" (H^1) matters (see the catalog).
* **Learn:** 7S ch. 7 (sheaves, gently); Hansen & Ghrist 2019 (`hansen2019spectral`) §2–3 for Laplacians; Curry's thesis (`curry2014sheaves`); Ghrist, *Elementary Applied Topology* ch. 9.

## 14. Kan extensions

Given `F : C → E` and `K : C → D`, the (left) **Kan extension** `Lan_K F : D → E` is the "best approximation" of extending `F` along `K`.

* **Example (speculative).** If you know a model's behaviour on single-hop queries (functor on generators) and want the *predicted* behaviour on composite queries, the free extension is Kan-extension-like. The gap between actual and extended behaviour is the composition defect. Also a possible formal home for "generalisation from verified claims to unverified ones".
* **Learn:** Riehl ch. 6; Leinster has only a little.

## 15. Topoi and internal logic

A **topos** is a category that behaves like sets but with an intuitionistic internal logic. **Subobject classifiers** give truth values that can be more than {true, false}.

* **Example (speculative).** Truth values of LLM claims are context-dependent, which is presheaf/topos-like. Mahadevan (`mahadevan2025topos`) proposes topos-theoretic architectures. For this survey it is mostly framing, with low feasibility.
* **Learn:** 7S ch. 7; Mac Lane & Moerdijk (advanced; not otherwise cited here).

## 16. Fibrations

A **(Grothendieck) fibration** `p : E → B` organises "objects over a base", e.g. data indexed by contexts, with reindexing along base morphisms.

* **Example (speculative).** Claims indexed by context or evidence set (open-book vs closed-book). Reindexing is "what the claim says under less evidence". Will's open- vs closed-book finding (the composition signal vanishes closed-book) is a question about how the signal behaves under change of base.
* **Learn:** nLab "Grothendieck fibration"; Jacobs, *Categorical Logic and Type Theory* (advanced; not otherwise cited here).

---

### How the concepts map to avenues

| Concept | Avenues in [02_avenues_catalog.md](02_avenues_catalog.md) |
|---|---|
| Functor / composition | A1–A9 |
| Markov categories / Kleisli | A2, A3, A5, P1–P5 |
| Enriched / metric (lax) functors | A4, A6 |
| Natural transformations | N1–N7 |
| Duals / dagger | D1–D3 |
| Sheaves / cohomology / Laplacians | S1–S8 |
| Galois connections / adjunctions | G1–G4 |
| Lenses / optics / open games | L1–L5 |
| Operads / monoidal | O1–O4 |
| Yoneda | Y1–Y2 |
| Kan extensions, topoi, fibrations | X1–X3 |
