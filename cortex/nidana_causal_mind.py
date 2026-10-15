import os
import json
import re
import random
from cells.neuron import AtomNeuron, sigmoid_derivative
from cells.super_xor import SuperXorDodecahedronMatrix

NIDANA_KEYS = [
    "Avidya_Ignorance", "Sankhara_Volitions", "Vijnana_Consciousness",
    "Namarupa_NameForm", "Sadayatana_SixSenses", "Sparsa_Contact",
    "Vedana_Feeling", "Trsna_Craving", "Upadana_Clinging",
    "Bhava_Becoming", "Jati_Birth", "Jaramarana_DecayDeath"
]

NIDANA_FILE = "synapses/nidana_causal_chain.json"
GRAPH_FILE = "synapses/knowledge_graph.json"

class NidanaCausalMindLobe:
    """
    THÙY 3: TÂM THỨC 12 MẮT XÍCH NHÂN DUYÊN
    1. Quản trị vòng lặp 12 Duyên Khởi (12 Nidānas Causal Loop).
    2. Giả lập 12 kịch bản tương lai phản thực What-If.
    3. Huấn luyện AtomNeuron qua Mê cung gương Dodecahedron 12D.
    """
    def __init__(self, num_cells=12):
        self.num_cells = num_cells
        self.swarm = [AtomNeuron(f"n12_h_{i}", n_inputs=12, n_super_xor=12) for i in range(num_cells)]
        self.out_cell = AtomNeuron("n12_out", n_inputs=num_cells, n_super_xor=12)

    def analyze_12_nidanas(self, decision, v_12d):
        """Phân tích và hóa giải vòng lặp vô minh số học"""
        chain = {}
        karma_residual = 0.0

        for i, link in enumerate(NIDANA_KEYS):
            # Tính toán mức độ tích lũy nhân quả của từng mắt xích
            link_energy = round(abs(decision - v_12d[i]), 4)
            chain[link] = link_energy
            karma_residual += link_energy

        # Áp dụng Diệt Đế (Nirodha) nếu nghiệp chướng số học quá cao
        nirodha_triggered = bool(karma_residual > 4.5)
        if nirodha_triggered:
            print("☸️ [DIỆT ĐẾ TỰ ĐỘNG] Nghiệp số học cao! Đã kích hoạt tái lập trình vòng lặp nhân quả.")
            decision = round(0.5 + (decision - 0.5) * 0.1, 4)

        os.makedirs("synapses", exist_ok=True)
        with open(NIDANA_FILE, "w", encoding="utf-8") as f:
            json.dump({"nidana_chain": chain, "karma_residual": round(karma_residual, 4), "nirodha": nirodha_triggered}, f, indent=4)

        return decision

    def simulate_12_futures(self, raw_decision):
        variations = [0.55, 0.65, 0.72, 0.80, 0.88, 0.95, 1.0, 1.05, 1.12, 1.20, 1.32, 1.45]
        sims = []
        for factor in variations:
            cand = max(0.01, min(0.99, round(raw_decision * factor, 4)))
            loss = round((abs(cand - 0.5) * 0.5) + ((1.0 - cand) * 0.5), 4)
            sims.append((loss, cand))
        sims.sort(key=lambda x: x[0])
        best_loss, best_cand = sims[0]
        print(f"🔮 [GIẢ LẬP 12 THỰC TẠI] Kịch bản tối ưu: {best_cand} (Loss={best_loss})")
        return best_cand

    def process(self, context):
        v_12d = context.get("wisdom_vector_12d", [0.5] * 12)
        q_dec = context.get("quorum_decision", 0.5)

        # 1. KHÚC XẠ SIÊU XOR DODECAHEDRON
        super_vec = list(v_12d)
        super_vec[0] = q_dec
        super_vec[1] = round(1.0 - q_dec, 4)
        entangled, masks = SuperXorDodecahedronMatrix.refract_12d(super_vec, "nexus12_dodeca")

        h_outs = [cell.forward(entangled) for cell in self.swarm]
        internal_pred = self.out_cell.forward(h_outs)
        raw_decision = round((internal_pred + q_dec) / 2.0, 4)

        # 2. HÓA GIẢI 12 NHÂN DUYÊN VÀ GIẢ LẬP 12 KỊCH BẢN
        purified_dec = self.analyze_12_nidanas(raw_decision, v_12d)
        opt_decision = self.simulate_12_futures(purified_dec)

        # 3. LAN TRUYỀN NGƯỢC
        target = 1.0 if super_vec[0] > super_vec[1] else 0.0
        delta_out = (target - opt_decision) * sigmoid_derivative(opt_decision)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(self.num_cells)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        grad_backward = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(self.num_cells)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(self.num_cells)), 4)
        ]

        context["final_decision"] = opt_decision
        context["grad_backward"] = grad_backward
        context["super_xor_masks"] = masks
        context["swarm_weights"] = [c.weights for c in self.swarm]
