# QuantU — Mathematical Reference

## 1. Newtonian Gravity

### Gravitational Force
$$\vec{F} = -\frac{GMm}{|\vec{r}|^2} \hat{r}$$

### Gravitational Potential
$$\Phi(\vec{r}) = -\frac{GM}{|\vec{r}|}$$

### Escape Velocity
$$v_{esc} = \sqrt{\frac{2GM}{r}}$$

## 2. Orbital Mechanics

### Vis-Viva Equation
$$v^2 = GM\left(\frac{2}{r} - \frac{1}{a}\right)$$

### Kepler's Third Law
$$T = 2\pi\sqrt{\frac{a^3}{GM}}$$

### Orbit Equation
$$r(\theta) = \frac{a(1-e^2)}{1 + e\cos\theta}$$

## 3. General Relativity

### Schwarzschild Metric
$$ds^2 = -\left(1 - \frac{r_s}{r}\right)c^2 dt^2 + \frac{dr^2}{1 - r_s/r} + r^2 d\Omega^2$$

where $r_s = 2GM/c^2$ is the Schwarzschild radius.

### Einstein Field Equations
$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$

### Geodesic Equation
$$\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = 0$$

## 4. Alcubierre Warp Metric (⚠️ Speculative)

$$ds^2 = -c^2 dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2$$

Shape function:
$$f(r_s) = \frac{\tanh(\sigma(r_s + R)) - \tanh(\sigma(r_s - R))}{2\tanh(\sigma R)}$$

## 5. Propulsion

### Tsiolkovsky Rocket Equation
$$\Delta v = v_e \ln\frac{m_0}{m_f}$$

### Ion Thrust
$$F = \dot{m} \cdot v_e = \frac{2\eta P}{v_e}$$

## 6. Numerical Methods

### Runge-Kutta 4th Order
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

### Velocity Verlet
$$x_{n+1} = x_n + v_n \Delta t + \frac{1}{2} a_n \Delta t^2$$
$$v_{n+1} = v_n + \frac{1}{2}(a_n + a_{n+1}) \Delta t$$
