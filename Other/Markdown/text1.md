# How to Calculate Loadings in PCA
## 🧠 What Are Loadings?
In PCA, **loadings** tell you how much each original variable contributes to each principal component.
They’re the **weights** (coefficients) in the linear combination that creates each component.
For example:
$$Z_1 = w_{1,1}X_1 + w_{1,2}X_2 + \dots + w_{1,p}X_p
$$
Here, the $w_{1,j}$ values are the **loadings** for the first principal component $Z_1$.
---
## ⚙️ How to Calculate Loadings (Step-by-Step)
Let’s assume your dataset $X$ has been standardized (mean = 0, variance = 1).
---
### Step 1️⃣ — Compute the Covariance (or Correlation) Matrix
If $X$ is your data matrix with shape $n \times p$ (n samples, p features):
$$\Sigma = \frac{1}{n - 1} X^T X
$$
- Each entry in $\Sigma$ shows how two variables vary together.
- If your data are on different scales, use the **correlation matrix** instead.
---
### Step 2️⃣ — Find Eigenvalues and Eigenvectors
Next, compute the **eigenvalues** and **eigenvectors** of the covariance matrix $\Sigma$:
$$\Sigma w = \lambda w
$$
- $\lambda$: eigenvalue → how much variance the component explains  
- $w$: eigenvector → direction of the component (the loadings)
You’ll get:
- $p$ eigenvalues (one per component)
- $p$ eigenvectors (each of length $p$)
---
### Step 3️⃣ — Normalize the Eigenvectors
Each eigenvector corresponds to one principal component.  
We usually normalize them to have **unit length** (sum of squares = 1).
These normalized eigenvectors are the **component loadings**.
$$\text{Loading matrix } = W = [w_1, w_2, ..., w_p]
$$
---
### Step 4️⃣ — Compute Principal Component Scores (optional)
Once you have the loadings, you can compute the **principal components (scores)**:
$$Z = X \cdot W
$$
Each column of $Z$ is a principal component (e.g., $Z_1, Z_2, \ldots$).
---
## 🧮 Example (Small Numeric Demo)
Say you have standardized data $X = \begin{bmatrix} X_1 & X_2 \end{bmatrix}$.
1. Compute covariance matrix:
$$\Sigma = \begin{bmatrix}
1.0 & 0.8 \\
0.8 & 1.0
\end{bmatrix}
$$
2. Find eigenvalues and eigenvectors:
   - Eigenvalues: $\lambda_1 = 1.8, \lambda_2 = 0.2$
   - Eigenvectors:
$$w_1 = \begin{bmatrix} 0.707 \\ 0.707 \end{bmatrix}, \quad
w_2 = \begin{bmatrix} -0.707 \\ 0.707 \end{bmatrix}
$$
3. So, **loadings matrix**:
$$W =
\begin{bmatrix}
0.707 & -0.707 \\
0.707 & 0.707
\end{bmatrix}
$$
Each column shows how strongly each variable contributes to each component.
---
## 🧩 Step 5️⃣ — Interpret the Loadings
- Large positive or negative loadings → that variable contributes strongly to the component.
- Small loadings → variable contributes little.
For example:
- If both $X_1$ and $X_2$ have large, positive loadings in $Z_1$, that component represents a **general trend** where both variables increase together.
- If one is positive and the other negative, the component represents a **contrast** between them.
---
