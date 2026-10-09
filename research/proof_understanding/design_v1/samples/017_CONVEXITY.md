# Sample 017: verified local parameter abstraction and invalid transfer

Source anchor: family 017, conclusion.tex, parameter-selection argument. The original text requires A^2<theta and nu(A-theta)>1-theta, followed by further auxiliary parameter construction. Its difficult interpolation theorem is not checked here.

## Claim contract
Given a rational-coefficient polynomial f(x)=sum_{i=1}^k w_i x^{r_i} with w_i>0, sum w_i=1, integer r_i>=2 and rational nu, the following are equivalent:
(1) There exist rational 0<theta<A<1 with f(A)<theta and nu(A-theta)>1-theta.
(2) nu>s/(s-1), where s=sum_i w_i*r_i.

## Mechanism and independent proof
Let s=f'(1)>1. For every integer r>=2,
x^r-r*x+(r-1)=(1-x)^2 sum_{j=0}^{r-2}(r-1-j)*x^j.
Therefore for 0<x<1,
f(x)-s*x+(s-1)=(1-x)^2 sum_i w_i sum_{j=0}^{r_i-2}(r_i-1-j)*x^j>0.
Hence (1-f(A))<s(1-A). Since theta>f(A) and theta<A, the ratio (A-theta)/(1-theta) is strictly less than (A-f(A))/(1-f(A)); the latter equals 1-(1-A)/(1-f(A)) and is strictly less than (s-1)/s. Multiplying by nu>0 forces nu>s/(s-1).

Conversely, rational A close enough to one satisfies nu(A-f(A))>1-f(A), by the slope limit. Because nu>1, upper=(nu*A-1)/(nu-1) is well-defined. Take rational theta strictly between f(A) and min(A,upper). Such an interval exists near A=1, proving sufficiency. Exact witnesses are constructible by A=1-2^(-k), then midpoint theta.

## Reusable insight and valid boundary
The numerical exponent r is not the invariant. In this convex-mixture class, the endpoint derivative s and the global tangent bound determine the critical threshold. For f=(x^2+x^4)/2 and g=(2x^2+x^5)/3, both s=3, so both have critical nu=3/2. The support of this result is the proved polynomial identity; the connection to pi is only its motivational source.

## Adversarial assumption intervention
Let h(x)=x^2-3*x^3*(1-x)^2. We have h(1)=1, h'(1)=2, h''(1)=-4, so the global convexity premise used above fails. Set nu=39/20, A=3/4, theta=31/64. Direct exact computation:
h(A)=495/1024 < 496/1024=theta;
nu*(A-theta)-(1-theta) = 3/1280 > 0.
Thus the system IS feasible even though nu<2. Blindly transferring the derivative-only rule would give an incorrect impossibility verdict. This is a genuine counterexample to an oversimplified abstract mechanism; it is NOT a counterexample to the source manuscript's theorem.

## Evidence and unknowns
Independent algebraic derivation and exact rational substitution establish all claims on this page. Python tests cover samples but do not replace the general proof. The high-level pi theorem, any interpolation extension and real-reader benefit are unverified.
