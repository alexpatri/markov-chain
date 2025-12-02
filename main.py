import numpy as np
from collections import Counter
import math

# -----------------------------------------------------------
# Definições dos estados
# -----------------------------------------------------------
states = {
    0: "Idle",                       # A
    1: "Jab",                        # B
    2: "Swing Right",                # C
    3: "Swing Left",                 # D
    4: "Hopping Stab",               # E
    5: "Hopping Swing",              # F
    6: "Hopping Stab High/Slow"      # G
}

# Matriz de transição da cadeia
P = np.array([
    [0.13, 0.16, 0.13, 0.00, 0.58, 0.00, 0.00],  # A
    [0.25, 0.50, 0.00, 0.25, 0.00, 0.00, 0.00],  # B
    [0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00],  # C
    [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # D
    [0.13, 0.00, 0.00, 0.00, 0.70, 0.04, 0.13],  # E
    [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # F
    [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]   # G
])

# -----------------------------------------------------------
# Simulação da Cadeia
# -----------------------------------------------------------
def simulate_chain(P, steps=10000, start_state=0):
    sequence = [start_state]
    current = start_state

    for _ in range(steps):
        current = np.random.choice(range(7), p=P[current])
        sequence.append(current)

    return sequence

sequence = simulate_chain(P, steps=10000, start_state=0)

# -----------------------------------------------------------
# 1. Probabilidade de cada ataque (distribuição empírica)
# -----------------------------------------------------------
counts = Counter(sequence)
total = len(sequence)

print("\n=== Probabilidade Empírica de Cada Estado (Ataques) ===")
for state_id, count in counts.items():
    print(f"{states[state_id]:<25} -> {count/total:.4f}")

# -----------------------------------------------------------
# 2. Identificação de padrões recorrentes
# (Transições frequentes)
# -----------------------------------------------------------
pair_counts = Counter((sequence[i], sequence[i+1]) for i in range(len(sequence)-1))

print("\n=== Transições Mais Frequentes (Padrões) ===")
for (s1, s2), c in pair_counts.most_common(10):
    print(f"{states[s1]} → {states[s2]} : {c}")

# -----------------------------------------------------------
# 3. Previsibilidade via entropia
# entropia média dos estados visitados
# -----------------------------------------------------------

def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

state_entropies = {i: entropy(P[i]) for i in range(7)}

# média ponderada pela frequência de visita
weighted_entropy = sum((counts[i] / total) * state_entropies[i] for i in range(7))

print("\n=== Entropia (Previsibilidade) ===")
for i in range(7):
    print(f"{states[i]:<25} -> Entropia: {state_entropies[i]:.4f}")

print(f"\nEntropia Média da Cadeia Durante a Luta: {weighted_entropy:.4f}")

max_entropy = np.log2(P.shape[0])
rel = weighted_entropy / max_entropy
rel = rel*100

print("\nEntropia máxima possível:")
print(f"  H_max = log2(7) = {max_entropy:.6f}")

print("\nProporção da entropia máxima:")
print(f"  H / H_max = {rel:.2f}%")

# Interpretação da previsibilidade
if rel < 25:
    interpret = "muito previsível"
elif rel < 70:
    interpret = "moderadamente previsível"
else:
    interpret = "pouco previsível"

print(f"\nInterpretação: O comportamento do chefe é {interpret}.")
