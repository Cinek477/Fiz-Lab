"""Wspólne wzory LaTeX dla Worda i źródła .tex."""
WZORY = {
 'I(x) = I0 [sin(α)/α]²,     α = πax/(λL)': r'I(x)=I_0\left(\frac{\sin\alpha}{\alpha}\right)^2,\qquad \alpha=\frac{\pi ax}{\lambda L}',
 'x_min,m = mλL/a;     |x_max,m| ≈ (m + 1/2)λL/a': r'x_{\min,m}=\frac{m\lambda L}{a},\qquad |x_{\max,m}|\approx\frac{(m+\frac12)\lambda L}{a}',
 'I_max,m/I0 ≈ 1/[π²(m + 1/2)²]': r'\frac{I_{\max,m}}{I_0}\approx\frac{1}{\pi^2\left(m+\frac12\right)^2}',
 'I(x) = I0 [sin(α)/α]² cos²(β),     β = πdx/(λL)': r'I(x)=I_0\left(\frac{\sin\alpha}{\alpha}\right)^2\cos^2\beta',
 'α = πax/(λL); β = πdx/(λL)': r'\alpha=\frac{\pi ax}{\lambda L},\qquad \beta=\frac{\pi dx}{\lambda L}',
 'r = (p_prawe − p_lewe)/2;     a_min = mλL/r;     a_max ≈ (m + 1/2)λL/r': r'r=\frac{p_{\mathrm{prawe}}-p_{\mathrm{lewe}}}{2},\quad a_{\min}=\frac{m\lambda L}{r},\quad a_{\max}\approx\frac{(m+\frac12)\lambda L}{r}',
 'r_m = (p_prawe,m − p_lewe,m)/2;     d_m = mλL/r_m': r'r_m=\frac{p_{\mathrm{prawe},m}-p_{\mathrm{lewe},m}}{2},\qquad d_m=\frac{m\lambda L}{r_m}',
 'uA(z średniego) = √[Σ(z_i − z średnie)² / (N(N − 1))]': r'u_{\mathrm A}(\bar z)=\sqrt{\frac{\sum_{i=1}^{N}(z_i-\bar z)^2}{N(N-1)}}',
 'u(r) = √[u(p_lewe)² + u(p_prawe)²]/2': r'u(r)=\frac12\sqrt{u^2(p_{\mathrm{lewe}})+u^2(p_{\mathrm{prawe}})}',
 'u(z)/z = √[(u(λ)/λ)² + (u(L)/L)² + (u(r)/r)²]': r'\frac{u(z)}{z}=\sqrt{\left(\frac{u(\lambda)}{\lambda}\right)^2+\left(\frac{u(L)}{L}\right)^2+\left(\frac{u(r)}{r}\right)^2}',
}
